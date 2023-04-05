#!/usr/bin/python3
"""This module contains the orders routes"""
from flask import Blueprint, render_template, url_for, flash, redirect
from inventory.models.product import Product
from inventory.models.user import User
from inventory.models.order import Order, OrderItem, Transaction
from inventory.orders.forms import OrderItemForm
from inventory import db
from flask_login import login_required, current_user

ord = Blueprint('orders', __name__)

@ord.route('/orders/new', methods=['GET', 'POST'])
def add_orders():
    """"This function defines the add orders route"""
    form = OrderItemForm()
    user = current_user
    if form.validate_on_submit():
        order_item = OrderItem(product=form.product.data, quantity=form.quantity.data)
        db.session.add(order_item)
        db.session.commit()
        flash('The order item has been added.', 'success')
        return redirect(url_for('orders.add_orders'))
    order_items = OrderItem.query.all()
    total = OrderItem.query.with_entities(db.func.sum(OrderItem.grandtotal)).scalar()
    return render_template('add_orders.html', title='Add Orders', form=form, order_items=order_items, total=total, user=user)
"""
@ord.route('/orders/create')
def create_orders():
    This function creates the order
    total = OrderItem.query.with_entities(db.func.sum(OrderItem.grandtotal)).scalar()
    order_items = OrderItem.query.all()
    order = Order(total=total, user=current_user)
    for order_item in order_items:
        order.order_items.append(order_item)
    db.session.add(order)
    db.session.commit()
    flash('The order has been created.', 'success')
    return redirect(url_for('orders.add_orders'))

@ord.route('/orders')
def orders():
    This function defines the orders route
    orders = Order.query.all()
    return render_template('orders.html', title='Orders', orders=orders)

@ord.route('/orders/<int:orderid>/print')
def print_order(orderid):
    This function defines the print order route
    order = Order.query.get_or_404(orderid)
    return render_template('print_order.html', title='Print Order', order=order)

@orders.route('/orders/<int:orderid>', methods=['GET', 'POST'])
def order(orderid):
    This function defines the order route
    order = Order.query.get_or_404(orderid)
    form = OrderItemForm()
    if form.validate_on_submit():
        order_item = OrderItem(product=form.product.data, quantity=form.quantity.data)
        order.order_items.append(order_item)
        db.session.commit()
        flash('The order item has been created.', 'success')
        return redirect(url_for('orders.order', orderid=order.id))
    return render_template('order.html', title='Order', order=order, form=form)

@orders.route('/orders/<int:orderid>/delete', methods=['POST'])
def delete_order(orderid):
    This function defines the delete order route
    order = Order.query.get_or_404(orderid)
    db.session.delete(order)
    db.session.commit()
    flash('The order has been deleted.', 'success')
    return redirect(url_for('orders.orders'))

@orders.route('/orders/<int:orderid>/order_items/<int:orderitemid>/delete', methods=['POST'])
def delete_order_item(orderid, orderitemid):
    This function defines the delete order item route
    order_item = OrderItem.query.get_or_404(orderitemid)
    db.session.delete(order_item)
    db.session.commit()
    flash('The order item has been deleted.', 'success')
    return redirect(url_for('orders.order', orderid=orderid))
"""
