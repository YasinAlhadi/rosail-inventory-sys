#!/usr/bin/python3
"""This module contains a user routes"""
from flask import Blueprint, render_template, url_for, flash, redirect, request
from inventory.users.forms import RegistrationForm, LoginForm
from inventory.models.user import User
from inventory import db, bcrypt, search
from flask_login import login_user, current_user, logout_user, login_required


users = Blueprint('users', __name__)


@users.route('/adduser', methods=['GET', 'POST'])
def adduser():
    """This function defines the adduser route
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))"""
    form = RegistrationForm()
    user = current_user
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(roleid=form.roleid.data, name=form.full_name.data, email=form.email.data,
                    password=hashed_password, phone=form.phone.data, address=form.address.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.full_name.data}!', 'success')
        return redirect(url_for('users.adduser'))
    return render_template('add_user.html', title='Register', form=form, user=user)


@users.route('/users_list')
@login_required
def users_list():
    """This function defines the users route"""
    users = User.query.all()
    return render_template('users.html', title='Users', users=users)


@users.route('/user_list/<int:user_id>/update', methods=['GET', 'POST'])
@login_required
def update_user(user_id):
    """This function defines the update user route"""
    user = User.query.get_or_404(user_id)
    form = RegistrationForm()
    if form.validate_on_submit():
        user.roleid = form.roleid.data
        user.name = form.full_name.data
        user.email = form.email.data
        user.phone = form.phone.data
        user.address = form.address.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.users_list'))
    elif request.method == 'GET':
        form.roleid.data = user.roleid
        form.full_name.data = user.name
        form.email.data = user.email
        form.phone.data = user.phone
        form.address.data = user.address
    return render_template('add_user.html', title='Update User', form=form, user=user)


@users.route('/user_list/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    """This function defines the delete user route"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('Your account has been deleted!', 'success')
    return redirect(url_for('users.users_list'))


@users.route('/search_results')
@login_required
def search_results():
    """This function defines the search results route"""
    user = current_user
    search = request.args.get('search')
    users = User.query.msearch(
        search, fields=['name', 'email'], limit=20).all()
    return render_template('user_search.html', title='Search Results', users=users, user=user)


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
            if user.roleid == 1:
                return redirect(url_for('main.dashboard'))
            else:
                return redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('singin.html', title='Login', form=form)


@users.route('/logout')
def logout():
    """This function defines the logout route"""
    logout_user()
    return redirect(url_for('users.login'))
