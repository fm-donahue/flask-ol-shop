from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import DecimalField, IntegerField, StringField, SubmitField
from wtforms.validators import URL, DataRequired, NumberRange
from wtforms.widgets import Input, TextArea


class AddItemForm(FlaskForm):
    item_name = StringField('Item Name', validators=[DataRequired()])
    picture = FileField('Item Picture', validators=[DataRequired(), 
                        FileAllowed(['jpg', 'png'])])
    brand = StringField('Brand', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired(),
                            NumberRange(min=1)],
                            widget=Input(input_type="number"))
    price = DecimalField('Price', places=2, validators=[DataRequired(),
                         NumberRange(min=1)], widget=Input(input_type="number"))
    order_details = StringField('Order Details', widget=TextArea())
    url = StringField("Item's Website", validators=[DataRequired(), URL()])
    submit = SubmitField('Add Item')
