#!/usr/bin/python3
"""This module contains the forms for the orders"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError
from inventory.models.order import Order, OrderItem, Transaction
from inventory.models.product import Product
from inventory.models.user import User


class OrderItemForm(FlaskForm):
    """This class defines the form for the order item"""
    product = SelectField('Product', coerce=int, validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Add to Order')

    def __init__(self, *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)
        self.product.choices = [(product.id, product.name) for product in Product.query.order_by('name')]
        
