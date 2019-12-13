import os
import string

import cloudinary.uploader
from flask import (Blueprint, abort, current_app, flash, jsonify, redirect,
                   render_template, request, url_for)
from flask_login import current_user, login_required

from shop_cart import basedir, db
from shop_cart.carts.forms import AddItemForm
from shop_cart.carts.utils import save_picture
from shop_cart.helpers import currency, round_up
from shop_cart.models import Cart, Order

carts = Blueprint('carts', __name__)


@carts.route('/')
@carts.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    shipping_fee = 3000
    php_rate = round_up(currency())
    page = request.args.get('page', 1, type=int)
    items = Cart.query.filter_by(user_id=current_user.get_id(), order=None) \
                      .order_by(Cart.date.desc()) \
                      .paginate(page=page, per_page=5)
    form = AddItemForm()
    if form.validate_on_submit():
        cart_items = Cart.query.filter_by(url=form.url.data).all()
        for cart_item in cart_items:
            if not cart_item.order:
                flash('Item already in cart. You can update your items!', 'danger')
                return redirect(url_for('carts.cart'))

        if form.picture.data:
            picture_file = save_picture(form.picture.data)

        cart = Cart(item_name=string.capwords(form.item_name.data),
                    brand=form.brand.data.upper(),
                    picture_file=picture_file, quantity=form.quantity.data,
                    price=form.price.data,
                    order_details=form.order_details.data,
                    url=form.url.data, user_id=current_user.id)
        db.session.add(cart)
        db.session.commit()

        pics_url = os.path.join(basedir, 'static/pics/' + picture_file)
        cloud_file, _ = os.path.splitext(picture_file)
        cloudinary.uploader.upload(f'{pics_url}',
                                   public_id=f'lilo_pics/{cloud_file}')

        flash('Item added!', 'success')
        return redirect(url_for('carts.cart'))
    return render_template('cart.html', shipping_fee=shipping_fee,
                           php_rate=php_rate, items=items, form=form)


@carts.route('/cart/<int:cart_id>/order', methods=['POST'])
@login_required
def order_item(cart_id):
    shipping_fee = 3000
    item = Cart.query.get_or_404(cart_id)
    if item.customer != current_user:
        abort(403)

    total_price = round_up(item.quantity * ((item.price * currency())
                           + shipping_fee))
    order = Order(total_price=total_price, balance=str(total_price),
                  shipping_fee=shipping_fee, user_id=item.customer.id,
                  cart_id=cart_id)

    item.php_rate = currency()
    db.session.add(order)
    db.session.commit()
    flash('Item ordered!', 'success')
    return redirect(url_for('carts.cart'))


@carts.route('/cart/<int:cart_id>/update', methods=['POST'])
@login_required
def update_item(cart_id):
    item = Cart.query.get_or_404(cart_id)
    if item.customer != current_user:
        abort(403)

    if request.form.get('quantity'):
        item.quantity = request.form.get('quantity')
        db.session.commit()

    if request.form.get('order_details'):
        item.order_details = request.form.get('order_details')
        db.session.commit()

    flash('Item updated.', 'success')
    return redirect(url_for('carts.cart'))


@carts.route('/async_update/<int:cart_id>', methods=['POST'])
def async_update(cart_id):
    item = Cart.query.get_or_404(cart_id)
    if item.customer != current_user:
        abort(403)

    json_data = request.get_json()
    item.quantity = int(json_data['quantity'])
    item.order_details = json_data['order_details']
    db.session.commit()
    return jsonify(None)


@carts.route('/cart/<int:cart_id>/delete', methods=['POST'])
@login_required
def delete_item(cart_id):
    item = Cart.query.get_or_404(cart_id)
    picture_path = os.path.join(current_app.root_path, 'static/pics',
                                item.picture_file)
    if item.customer != current_user:
        abort(403)
    db.session.delete(item)
    db.session.commit()
    os.remove(picture_path)
    flash('Item deleted!', 'success')
    return redirect(url_for('carts.cart'))
