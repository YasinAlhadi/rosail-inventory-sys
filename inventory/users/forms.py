#!/usr/bin/python3
"""This module contains the user's forms"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from inventory.models.user import User



class RegistrationForm(FlaskForm):
    """This class defines the registration form"""
    roleid = SelectField('Role', choices=[(1, 'Admin'), (2, 'User')], validators=[DataRequired()])
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=4, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=2, max=20)])
    address = StringField('Address', validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        """This function validates the email"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')
    
    def validate_phone(self, phone):
        """This function validates the phone"""
        user = User.query.filter_by(phone=phone.data).first()
        if user:
            raise ValidationError('That phone is exist. Please choose a different one.')


class LoginForm(FlaskForm):
    """This class defines the login form"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
