from flask import abort

from shop_cart.helpers import phone_number_format


def check_phone_number(number):
    phone_number = phone_number_format(number)
    if not phone_number:
        abort(400, description='Incorrect phone number.')
    return phone_number
