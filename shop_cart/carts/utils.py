import os
import secrets

from flask import current_app
from PIL import Image


def save_picture(form_picture):
    random_fname = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fname = random_fname + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/pics',
                                picture_fname)
    output_size = (512, 512)
    image = Image.open(form_picture)
    image.thumbnail(output_size)
    image.save(picture_path)
    return picture_fname
