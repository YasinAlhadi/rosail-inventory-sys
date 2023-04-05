#!/usr/bin/python3
"""This module contains the main routes"""
from flask import Blueprint, render_template, url_for, flash, redirect
from inventory.models.user import User
from flask_login import login_required, current_user, login_user, logout_user

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    if current_user.is_authenticated:
        return render_template('home.html', title='Home', user=current_user)
    """This function defines the home route"""
    """if current_user.roleid == 1:
        return render_template('login.html', title='Login')"""
    return redirect(url_for('users.login'))

@main.route('/about')
def about():
    """This function defines the about route"""
    return render_template('about.html', title='About')

@main.route('/dashboard')
def dashboard():
    """This function defines the dashboard route"""
    return render_template('dashboard.html', title='Dashboard')
    