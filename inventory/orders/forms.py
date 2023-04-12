#!/usr/bin/python3
"""This module contains the forms for the orders"""
from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField
from wtforms.validators import DataRequired


class OrderItemForm(FlaskForm):
    """This class defines the form for the order item"""
    quantity = IntegerField('Quantity', validators=[DataRequired()], default=1)
    submit = SubmitField('Add to Order')
