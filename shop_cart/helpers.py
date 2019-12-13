import os
from math import ceil

import cloudinary.uploader
import requests
from flask import abort
from flask_admin.form import ImageUploadField


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"


def php(value):
    """Format value as PHP."""
    return f"₱{value:,.2f}"


def transaction_id(order_id):
    """Format transaction id"""
    return f"{order_id:08d}"


def date_format(date):
    """Format date"""
    return date.strftime('%d %b %Y')


def phone_number_format(number):
    """Format mobile number"""
    for num in number:
        if num.isalpha():
            return None

    if number[:2] == '09':
        number = ''.join(char for char in number if char.isdigit())
        if len(number) != 11:
            return None

        formatted_num = '(+63) '

        for index, num in enumerate(number[1:]):
            formatted_num += num
            if index % 3 == 0 and 7 > index > 0:
                formatted_num += '-'
        return formatted_num

    return None


def currency():
    """Look for currency rate USD"""

    # Contact API
    try:
        currency_api_key = os.environ.get('liloshipping_currency_api_key')
        response = requests.get('https://free.currconv.com/api/v7/convert?q=USD_PHP&compact=ultra&apiKey=' + currency_api_key)
        response.raise_for_status()
    except requests.RequestException:
        abort(500, description='Currency API request failed.')

    # Parse response
    try:
        quote = response.json()
        return round_up(quote['USD_PHP'])

    except (KeyError, TypeError, ValueError):
        return None


def round_up(value):
    return ceil(value * 100) / 100


class CloudinaryImageUpload(ImageUploadField):
    def _save_image(self, image, path, format='JPEG'):
        super()._save_image(image=image, path=path)

        image_name = (os.path.split(path)[1]).split('.')
        cloudinary.uploader.upload(f'{path}',
                                   public_id=f'lilo_pics/{image_name[0]}')
