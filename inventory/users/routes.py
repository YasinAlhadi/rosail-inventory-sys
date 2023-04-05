#!/usr/bin/python3
"""This module contains a user routes"""
from flask import Blueprint, render_template, url_for, flash, redirect, request
from inventory.users.forms import RegistrationForm, LoginForm
from inventory.models.user import User
from inventory import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required


users = Blueprint('users', __name__)

@users.route('/adduser', methods=['GET', 'POST'])
def adduser():
    """This function defines the adduser route
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))"""
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(roleid=form.roleid.data, name=form.full_name.data, email=form.email.data, password=hashed_password, phone=form.phone.data, address=form.address.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.full_name.data}!', 'success')
        return redirect(url_for('users.adduser'))
    return render_template('adduser.html', title='Register', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    """This function defines the login route"""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            """next_page = request.args.get('next')"""
            return redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route('/logout')
def logout():
    """This function defines the logout route"""
    logout_user()
    return redirect(url_for('users.login'))
