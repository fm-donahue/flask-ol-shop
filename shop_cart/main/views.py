from flask import Blueprint, render_template

main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@main.route('/about_us', methods=['GET'])
def about():
    return render_template('about.html')


@main.route('/contact_us', methods=['GET'])
def contact():
    return render_template('contact.html')


@main.route('/prohibited_items', methods=['GET'])
def prohibited():
    return render_template('prohibited.html')
