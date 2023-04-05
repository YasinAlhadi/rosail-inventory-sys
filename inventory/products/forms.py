#!/usr/bin/python3
"""This module contains the forms for the products"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError
from inventory.models.product import Product, Category, Brand

class ProductForm(FlaskForm):
    """This class defines the form for the product"""
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=128)])
    price = FloatField('Price', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    category = SelectField('Category', coerce=int, validators=[DataRequired()])
    brand = SelectField('Brand', coerce=int, validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=2, max=128)])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name) for category in Category.query.order_by('name')]
        self.brand.choices = [(brand.id, brand.name) for brand in Brand.query.order_by('name')]

    def validate_name(self, name):
        """This function validates the name of the product"""
        product = Product.query.filter_by(name=name.data).first()
        if product:
            raise ValidationError('The name of this product exists. Please choose a different one.')

class CategoryForm(FlaskForm):
    """This class defines the form for the category"""
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=128)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=2, max=128)])
    submit = SubmitField('Submit')

    def validate_name(self, name):
        """This function validates the name of the category"""
        category = Category.query.filter_by(name=name.data).first()
        if category:
            raise ValidationError('That name is already taken. Please choose a different one.')

class BrandForm(FlaskForm):
    """This class defines the form for the brand"""
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=128)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=2, max=128)])
    submit = SubmitField('Submit')

    def validate_name(self, name):
        """This function validates the name of the brand"""
        brand = Brand.query.filter_by(name=name.data).first()
        if brand:
            raise ValidationError('That name is already taken. Please choose a different one.')