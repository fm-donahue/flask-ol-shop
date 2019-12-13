from flask import Flask
from flask_admin import Admin, AdminIndexView
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from shop_cart.config import Config
from shop_cart.helpers import date_format, php, round_up, transaction_id, usd

import os

basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
mail = Mail()
admin = Admin(
    template_mode='bootstrap3',
    index_view=AdminIndexView(
        template='admin/index.html'
    )
)
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    mail.init_app(app)
    admin.init_app(app)
    login_manager.init_app(app)

    from shop_cart.carts.views import carts
    from shop_cart.users.views import users
    from shop_cart.shipments.views import ship
    from shop_cart.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(carts)
    app.register_blueprint(ship)
    app.register_blueprint(errors)

    # Ensure responses aren't cached
    @app.after_request
    def after_request(response):
        response.headers['Cache-Control'] = 'no-cache, no-store, \
                                            must-revalidate'
        response.headers['Expires'] = 0
        response.headers['Pragma'] = 'no-cache'
        return response

    # Custom filters
    app.jinja_env.filters["usd"] = usd
    app.jinja_env.filters["php"] = php
    app.jinja_env.filters["transaction_id"] = transaction_id
    app.jinja_env.filters["date_format"] = date_format
    app.jinja_env.filters["round_up"] = round_up

    return app
