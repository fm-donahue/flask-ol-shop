import os
import re
import secrets
from datetime import datetime

from flask import Flask, Markup, abort, current_app, session, url_for
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import ImageUploadField
from flask_admin.menu import MenuLink
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from wtforms import validators

from shop_cart import admin, db, login_manager

app = Flask(__name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class MyModelView(ModelView):
    def is_accessible(self):
        try:
            return session['is_admin']
        except (KeyError):
            abort(404)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(18), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    items = db.relationship('Cart', backref='customer', lazy='dynamic')
    orders = db.relationship('Order', backref='customer', lazy='dynamic')

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return
        return User.query.get(user_id)

    def __str__(self):
        return f"{self.first_name} {self.last_name}, User ID:{self.id}"

    def __repr__(self):
        return f"User('{self.first_name}, {self.last_name}, {self.email}')"


class UserView(MyModelView):
    can_edit = True
    can_delete = False
    column_list = ['id', 'first_name', 'last_name', 'email', 'phone_number']
    column_filters = ['id', 'first_name', 'last_name', 'email']
    form_columns = ['first_name', 'last_name', 'password', 'phone_number', 'is_admin']


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(20), nullable=False)
    picture_file = db.Column(db.String(20), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    php_rate = db.Column(db.Float(precision=2))
    order_details = db.Column(db.String(200))
    url = db.Column(db.String(2048), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order = db.relationship('Order', backref='cart', uselist=False)

    def __str__(self):
        return f"User ID:{self.customer.id}, Cart(ID:{self.id}, {self.item_name})"

    def __repr__(self):
        return f"Cart('{self.item_name}, {self.brand}, {self.picture_file}, \
{self.quantity}, {self.price}, {self.date}')"


class CartView(MyModelView):
    can_create = False
    can_edit = False
    column_list = ['user_id', 'id', 'item_name', 'brand', 'picture_file',
                   'quantity', 'price', 'php_rate', 'order_details', 'url', 'date']
    column_sortable_list = ['id', 'user_id', 'date']
    column_default_sort = ('date', True)
    column_filters = ['id', 'user_id']

    def text_formatter(view, context, model, name):
        return model.item_name[:20]

    def view_picture(view, context, model, name):
        if not model.picture_file:
            return ''
        return Markup('<a href="#viewPictureModal{0}" data-toggle="modal">'
                      'View Image'
                      '</a>'
                        '<div class="modal fade" id="viewPictureModal{0}" tabindex="-1" \
                            role="dialog" aria-labelledby="viewPictureModalLabel{0}">'
                            '<div class="modal-dialog" role="document">'
                                '<div class="modal-content">'
                                    '<div class="modal-body">'
                                        '<img src={1}>'
                                    '</div>'
                                    '<div class="modal-footer">'
                                        '<button type="button" class="btn btn-default" \
                                        data-dismiss="modal">Close</button>'
                                    '</div>'
                                '</div>'
                            '</div>'
                        '</div>'.format(model.id, url_for('static', filename='pics/' + model.picture_file)))

    def view_details(view, context, model, name):
        if not model.order_details:
            return ''

        return Markup('<a href="#orderDetailsModal{0}" data-toggle="modal">'
                      'View Details'
                      '</a>'
                        '<div class="modal fade" id="orderDetailsModal{0}" tabindex="-1" \
                            role="dialog" aria-labelledby="orderDetailsModalLabel{0}">'
                            '<div class="modal-dialog" role="document">'
                                '<div class="modal-content">'
                                    '<div class="modal-body">'
                                        '{1}'
                                    '</div>'
                                    '<div class="modal-footer">'
                                        '<button type="button" class="btn btn-default" \
                                        data-dismiss="modal">Close</button>'
                                    '</div>'
                                '</div>'
                            '</div>'
                        '</div>'.format(model.id, model.order_details))

    def view_url(view, context, model, name):
        if not model.url:
            return ''
        return Markup(f"<a href='{model.url}' target='_blank'>Go To Url</a>")

    column_formatters = {
        'item_name': text_formatter,
        'picture_file': view_picture,
        'order_details': view_details,
        'url': view_url
    }


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_price = db.Column(db.Float(precision=2), nullable=False)
    balance = db.Column(db.String(10))
    shipping_fee = db.Column(db.Integer)
    order_status = db.Column(db.String(10), nullable=False, default='PENDING')
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    paid = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), unique=True)
    shipment = db.relationship('Shipment', backref='order', uselist=False)

    def __str__(self):
        return f"User(ID:{self.customer.id}, {self.customer.last_name}) \
Cart(ID:{self.cart.id}, {self.cart.item_name})"

    def __repr__(self):
        return f"Order('{self.customer}, {self.cart_id}, {self.order_status}, \
{self.order_date}')"


class OrderView(MyModelView):
    can_create = False
    column_list = ['id', 'user_id', 'cart_id', 'total_price', 'balance',
                   'shipping_fee', 'order_status', 'order_date', 'paid']
    column_sortable_list = ['id', 'user_id', 'order_status', 'order_date', 'paid']
    column_default_sort = ('order_date', True)
    column_filters = ['id', 'user_id', 'order_status']
    form_choices = {
        'order_status': [
            ('PENDING', 'PENDING'),
            ('REJECTED', 'REJECTED'),
            ('CANCELLED', 'CANCELLED'),
            ('ACCEPTED', 'ACCEPTED'),
            ('IN TRANSIT', 'IN TRANSIT'),
            ('DELIVERED', 'DELIVERED')
        ]
    }

    # def on_model_change(self, form, model, is_created):
    #     if not is_created:
    #         if model.balance != form.balance.data:
    #             if len(re.findall('-', form.balance.data)) == 1:
    #                 num_list = list(map(float, re.split('[-\s]+', form.balance.data)))
    #                 if len(num_list) == 2:
    #                     new_balance = num_list[0] - num_list[1]
    #                     if new_balance >= 0:
    #                         model.balance = str(new_balance)
    #                         db.session.commit()
    #                         return

    #             raise validators.ValidationError('Incorrect input')
    #     return


class Shipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tracking_number = db.Column(db.String)
    estimated_date = db.Column(db.Date)
    picture1 = db.Column(db.String(25))
    picture2 = db.Column(db.String(25))
    picture3 = db.Column(db.String(25))
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Shipment('{self.tracking_number}, {self.estimated_date}, \
{self.order_id}, {self.user_id}')"


def picture_name(obj, file_data):
    _, f_ext = os.path.splitext(file_data.filename)
    return f'{str(secrets.token_hex(8))}{f_ext}'


class ShipmentView(MyModelView):
    can_delete = False
    column_list = ['user_id', 'order_id', 'id', 'tracking_number', 'picture1',
                   'picture2', 'picture3', 'estimated_date']
    column_sortable_list = ['user_id', 'order_id', 'id', 'tracking_number',
                            'estimated_date']
    column_default_sort = ('estimated_date', True)
    column_filters = ['id', 'user_id', 'order_id', 'tracking_number']

    def _list_thumbnail(view, context, model, name):
        pic_list = {'picture1': model.picture1, 'picture2': model.picture2,
                    'picture3': model.picture3}
        if not pic_list.get(name):
            return ''

        return Markup("<a href='{}' target='_blank'>View Image</a>"
                      .format(url_for('static', filename=f'{pic_list.get(name)}')))

    def upload_image(num):
        return ImageUploadField(f'Picture{num}',
                                base_path=os.path.join(app.root_path, 'static'),
                                relative_path='pics/',
                                namegen=picture_name,
                                max_size=(512, 512, False))

    column_formatters = {
        'picture1': _list_thumbnail,
        'picture2': _list_thumbnail,
        'picture3': _list_thumbnail
    }

    form_extra_fields = {
        'picture1': upload_image(1),
        'picture2': upload_image(2),
        'picture3': upload_image(3)
    }


@db.event.listens_for(Order, 'after_update')
def add_shipment(mapper, connection, target):
    shipment_table = Shipment.__table__
    if target.order_status == ('ACCEPTED') and not target.shipment:
        connection.execute(shipment_table.insert().values(order_id=target.id,
                           user_id=target.user_id))


admin.add_view(UserView(User, db.session))
admin.add_view(CartView(Cart, db.session))
admin.add_view(OrderView(Order, db.session))
admin.add_view(ShipmentView(Shipment, db.session))
admin.add_link(MenuLink(name='Logout', url='/logout'))
