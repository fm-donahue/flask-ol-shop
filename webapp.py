from shop_cart import create_app, db
from shop_cart.models import Cart, Order, Shipment, User

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Cart': Cart, 'Order': Order, 'Shipment': Shipment}


if __name__ == '__main__':
    app.run()
