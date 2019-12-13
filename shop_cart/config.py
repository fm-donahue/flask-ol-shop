import os


class Config:
    SECRET_KEY = os.environ.get('liloshipping_secret_key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('lilo_database_uri')
    SQLALCHEMY_ECHO = True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('lilo_mail_user')
    MAIL_PASSWORD = os.environ.get('lilo_mail_password')
    FLASK_ADMIN_SWATCH = 'simplex'
    ADMIN_USER = os.environ.get('liloshipping_admin_user')
    ADMIN_PASSWORD = os.environ.get("liloshipping_admin_password")
    TEMPLATES_AUTO_RELOAD = True
    CLOUDINARY_URL = os.environ.get('cloudinary_url')
