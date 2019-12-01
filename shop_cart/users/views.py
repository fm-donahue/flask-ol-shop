import re
import string

from flask import (Blueprint, current_app, flash, json, redirect,
                   render_template, request, session, url_for)
from flask_login import current_user, login_required, login_user, logout_user
from flask_mail import Message

from shop_cart import bcrypt, db, mail
from shop_cart.models import User
from shop_cart.users.forms import (AccountForm, LoginForm, RegistrationForm,
                                   RequestResetPasswordForm, ResetPasswordForm)
from shop_cart.users.utils import check_phone_number

users = Blueprint('users', __name__)


@users.route('/check_email', methods=['GET'])
def check_email():
    """Return true if email is available, else false, in JSON format"""
    email = request.args.get('email')
    if re.match('[^@]+@[^@]+\.[^@]+', email):
        if User.query.filter_by(email=email).first():
            return json.dumps(False)
        else:
            return json.dumps(True)
    return json.dumps(None)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('cart'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).\
            decode('utf-8')
        user = User(first_name=string.capwords(form.first_name.data),
                    last_name=string.capwords(form.last_name.data),
                    email=form.email.data,
                    phone_number=check_phone_number(form.phone_number.data),
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account Created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('carts.cart'))
    try:
        if session['is_admin']:
            return redirect(url_for('admin.index'))
    except (KeyError):
        form = LoginForm()
        if form.validate_on_submit():
            if form.email.data == current_app.config['ADMIN_USER'] and \
                                bcrypt.check_password_hash(
                                current_app.config['ADMIN_PASSWORD'],
                                form.password.data):
                session['is_admin'] = True
                return redirect(url_for('admin.index'))
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password,
                                                   form.password.data):
                login_user(user, remember=form.rememberMe.data)
                next_page = request.args.get('next')
                if user.is_admin:
                    return redirect(url_for('admin.index'))
                return redirect(next_page or url_for('users.login'))
            else:
                flash('Login Unsuccessful. Please check email and password.',
                      'danger')
        return render_template('login.html', form=form)


@users.route('/logout')
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('users.login'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = AccountForm()
    if form.validate_on_submit():
        user = User.query.get(current_user.get_id())
        if bcrypt.check_password_hash(user.password, form.password.data):
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            current_user.email = form.email.data
            current_user.phone_number = check_phone_number(form.phone_number.data)
            db.session.commit()
            flash('Account Updated!', 'success')
            return redirect(url_for('users.account'))
        else:
            flash('Incorrect password! Please try again.', 'danger')
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.phone_number.data = current_user.phone_number\
            .replace('(+63) ', '0').replace('-', '')
    return render_template('account.html', form=form)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

Ignore this if you did not make this request.
'''
    mail.send(msg)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('carts.cart'))
    form = RequestResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions on how to reset your \
              password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('carts.cart'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Invalid or expired token.', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).\
            decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('You have changed your password. You are now able to login.',
              'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', form=form)
