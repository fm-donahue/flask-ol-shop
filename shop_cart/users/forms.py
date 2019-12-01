from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import (DataRequired, Email, EqualTo, Length, Regexp,
                                ValidationError)

from shop_cart.models import User


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[DataRequired(),
                Regexp('^(?:0|\+?\(?63\)?)((?:-)?(?:\s)?(?:[9]))((?:-)?(?:\s)?(?:\d)){9}$'),
                Length(min=11)])
    password = PasswordField('Password', validators=[DataRequired(), 
                Regexp('^(?=.+[a-zA-Z])(?=.+[\d])([a-zA-z\d]){8,16}$', 
                message='Must contain 8-16 characters with at least 1 number.'),
                Length(min=8, max=16)])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email is taken. Please use a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    rememberMe = BooleanField('Remember Me')
    submit = SubmitField('Login')


class AccountForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[DataRequired(),
                               Length(min=11)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Save Changes')

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('Email is taken. Please use a different one.')


class RequestResetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Reset Password')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('This email is not registered! You must \
                                  create first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(),
                Regexp('^(?=.+[a-zA-Z])(?=.+[\d])([a-zA-z\d]){8,16}$',
                message='Must contain a minimum of 8 characters with at least 1 \
                number.'), Length(min=8, max=16)])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
