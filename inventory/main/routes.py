#!/usr/bin/python3
"""This module contains the main routes"""
from flask import Blueprint, render_template, url_for, flash, redirect
from inventory.models.user import User
from inventory.models.product import Product
from inventory.orders.forms import OrderItemForm
from flask_login import login_required, current_user, login_user, logout_user

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    """This function defines the home route"""
    form = OrderItemForm()
    products = Product.query.all()
    if current_user.is_authenticated:
        return render_template('home.html', title='Home', user=current_user, products=products, form=form)
    else:
        return redirect(url_for('users.login'))


@main.route('/dashboard')
@login_required
def dashboard():
    """This function defines the dashboard route"""
    if current_user.id == 1:
        return render_template('dashboard.html', title='Dashboard', user=current_user)
    else:
        flash('You do not have access to this page', 'danger')
        return redirect(url_for('main.home'))
