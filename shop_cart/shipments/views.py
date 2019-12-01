from flask import Blueprint, render_template, request
from flask_login import current_user, login_required

from shop_cart.models import Order

ship = Blueprint('ship', __name__)


@ship.route('/shipments/<sub_nav>', methods=['GET'])
@login_required
def shipments(sub_nav):
    page = request.args.get('page', 1, type=int)
    if sub_nav == 'all':
        orders = Order.query.filter_by(user_id=current_user.get_id()) \
                            .order_by(Order.order_date.desc()) \
                            .paginate(page=page, per_page=5)
    elif sub_nav == 'pending_payment':
        orders = Order.query.filter_by(user_id=current_user.get_id()) \
                            .filter(Order.order_status.in_(['PENDING',
                                    'REJECTED', 'CANCELLED'])) \
                            .order_by(Order.order_date.desc()) \
                            .paginate(page=page, per_page=5)
    elif sub_nav == 'prepare_shipment':
        orders = Order.query.filter_by(user_id=current_user.get_id(),
                                       order_status='ACCEPTED') \
                                       .order_by(Order.order_date.desc()) \
                                       .paginate(page=page, per_page=5)
    elif sub_nav == 'on_its_way':
        orders = Order.query.filter_by(user_id=current_user.get_id(),
                                       order_status='IN TRANSIT') \
                                       .order_by(Order.order_date.desc()) \
                                       .paginate(page=page, per_page=5)
    else:
        orders = Order.query.filter_by(user_id=current_user.get_id(),
                                       order_status='DELIVERED') \
                                       .order_by(Order.order_date.desc()) \
                                       .paginate(page=page, per_page=5)
    return render_template('shipments.html', orders=orders)
