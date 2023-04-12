#!/usr/bin/python3
"""This module contains the orders routes"""
from flask import Blueprint, render_template, url_for, flash, redirect, request, session
from inventory.models.product import Product
from inventory.models.user import User
from inventory.models.order import Orders
from inventory.orders.forms import OrderItemForm
from inventory import db
from flask_login import login_required, current_user
from datetime import datetime

ord = Blueprint('orders', __name__)

"""
@ord.route('/order')
@login_required
def order():
    This function creates an order
    form = OrderItemForm()
    products = Product.query.all()
    user = current_user
    return render_template('create_order.html', title='Create Order', form=form, products=products, user=user)
"""


@ord.route('/order', methods=['POST'])
@login_required
def create_order():
    """This function adds a product to the order"""
    form = OrderItemForm()
    name_p = request.form.get('name_p')
    product = Product.query.filter_by(name=name_p).first()
    quantity = int(request.form.get('quantity'))
    print(quantity)
    print(product)
    if product and quantity and request.method == 'POST':
        items = {product.name: {'name': product.name, 'price': product.price,
                                'quantity': quantity, 'total': product.price * quantity}}
        all_total_price = 0
        all_total_quantity = 0

        session.modified = True

        if 'items' in session:
            if product.name in session['items']:
                for key, value in session['items'].items():
                    if key == product.name:
                        value['quantity'] += quantity
                        value['total'] = value['price'] * value['quantity']
            else:
                session['items'] = merge_dicts(session['items'], items)
            for key, value in session['items'].items():
                all_total_price += value['total']
                all_total_quantity += value['quantity']
        else:
            session['items'] = items
            all_total_price = product.price * quantity
            all_total_quantity = quantity
        session['all_total_price'] = all_total_price
        session['all_total_quantity'] = all_total_quantity
        flash('Product added to order', 'success')
        return redirect(url_for('main.home'))
    flash('Product not added to order', 'danger')
    return redirect(url_for('main.home'))


@ord.route('/order/view_order')
@login_required
def view_order():
    """This function displays the order"""
    user = current_user
    if 'items' in session:
        return render_template('view_order.html', title='View Order', user=user)
    flash('No items in order', 'danger')
    return redirect(url_for('main.home', user=user))


@ord.route('/order/completed_order')
@login_required
def completed_order():
    """save the order to the database"""
    user = current_user
    if current_user.is_authenticated:
        user_id = user.id
        invoice = 'RMS' + str(user_id) + \
            str(datetime.now().strftime('%Y%m%d%H%M%S'))
        order = Orders(user_id=user_id, invoice_number=invoice, order=session['items'],
                       total_price=session['all_total_price'],
                       quantity=session['all_total_quantity'])
        db.session.add(order)
        db.session.commit()
        session.pop('items')
        flash('Order completed', 'success')
        return redirect(url_for('orders.invoice', invoice=invoice, user=user))
    flash('Order not completed', 'danger')
    return redirect(url_for('orders.order'), user=user)


@ord.route('/order/invoices')
@login_required
def invoices():
    """This function displays the invoices"""
    user = current_user
    users = User.query.all()
    orders = Orders.query.all()
    return render_template('invoices.html', title='Invoice', user=user, users=users, orders=orders)


@ord.route('/order/invoice/<string:invoice>')
@login_required
def invoice(invoice):
    """This function displays the invoice"""
    user = current_user
    user_id = user.id
    c_user = User.query.filter_by(id=user_id).first()
    order = Orders.query.filter_by(invoice_number=invoice).first()
    return render_template('invoice.html', title='Invoice', order=order, user=user, c_user=c_user)


@ord.route('/order/cancel_order')
@login_required
def cancel_order():
    """This function cancels the order"""
    session.pop('items')
    flash('Order cancelled', 'success')
    return redirect(url_for('orders.order'))


@ord.route('/order/delete_item/<string:name>', methods=['POST'])
@login_required
def delete_item(name):
    """This function deletes an item from the order"""
    if 'items' in session:
        for key, value in session['items'].items():
            if key == name:
                del session['items'][key]
                break
        flash('Item deleted', 'success')
        return redirect(url_for('orders.view_order'))
    flash('Item not deleted', 'danger')
    return redirect(url_for('orders.view_order'))


def merge_dicts(dict1, dict2):
    """This function merges two dictionaries"""
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    elif isinstance(dict1, set) and isinstance(dict2, set):
        return dict1.union(dict2)
    return False
