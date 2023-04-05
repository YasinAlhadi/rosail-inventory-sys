#!/usr/bin/python3
"""This module contains the orders routes"""
from flask import Blueprint, render_template, url_for, flash, redirect
from inventory.models.product import Product
from inventory.models.user import User
from inventory.models.order import Order, OrderItem, Transaction
from inventory.orders.forms import OrderForm, OrderItemForm
from inventory import db
from flask_login import login_required, current_user

orders = Blueprint('orders', __name__)

@orders.route('/orders', methods=['GET', 'POST'])
@login_required
def orders():
    """This function defines the orders route"""
    form = OrderForm()
    if form.validate_on_submit():
        order = Order(customer=form.customer.data)
        db.session.add(order)
        db.session.commit()
        flash('The order has been created.', 'success')
        return redirect(url_for('orders.order', orderid=order.id))
    return render_template('orders.html', title='Orders', form=form)

@orders.route('/orders/<int:orderid>', methods=['GET', 'POST'])
@login_required
def order(orderid):
    """This function defines the order route"""
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
@login_required
def delete_order(orderid):
    """This function defines the delete order route"""
    order = Order.query.get_or_404(orderid)
    db.session.delete(order)
    db.session.commit()
    flash('The order has been deleted.', 'success')
    return redirect(url_for('orders.orders'))

@orders.route('/orders/<int:orderid>/order_items/<int:orderitemid>/delete', methods=['POST'])
@login_required
def delete_order_item(orderid, orderitemid):
    """This function defines the delete order item route"""
    order_item = OrderItem.query.get_or_404(orderitemid)
    db.session.delete(order_item)
    db.session.commit()
    flash('The order item has been deleted.', 'success')
    return redirect(url_for('orders.order', orderid=orderid))

@orders.route('/orders/<int:orderid>/order_items/<int:orderitemid>/checkout', methods=['POST'])
@login_required
def checkout_order_item(orderid, orderitemid):
    """This function defines the checkout order item route"""
    order_item = OrderItem.query.get_or_404(orderitemid)
    order_item.checkout()
    db.session.commit()
    flash('The order item has been checked out.', 'success')
    return redirect(url_for('orders.order', orderid=orderid))

@orders.route('/orders/<int:orderid>/checkout', methods=['POST'])
@login_required
def checkout_order(orderid):
    """This function defines the checkout order route"""
    order = Order.query.get_or_404(orderid)
    order.checkout()
    db.session.commit()
    flash('The order has been checked out.', 'success')
    return redirect(url_for('orders.orders'))

@orders.route('/orders/<int:orderid>/order_items/<int:orderitemid>/return', methods=['POST'])
@login_required
def return_order_item(orderid, orderitemid):
    """This function defines the return order item route"""
    order_item = OrderItem.query.get_or_404(orderitemid)
    order_item.return_()
    db.session.commit()
    flash('The order item has been returned.', 'success')
    return redirect(url_for('orders.order', orderid=orderid))

@orders.route('/orders/<int:orderid>/return', methods=['POST'])
@login_required
def return_order(orderid):
    """This function defines the return order route"""
    order = Order.query.get_or_404(orderid)
    order.return_()
    db.session.commit()
    flash('The order has been returned.', 'success')
    return redirect(url_for('orders.orders'))

@orders.route('/orders/<int:orderid>/order_items/<int:orderitemid>/refund', methods=['POST'])
@login_required
def refund_order_item(orderid, orderitemid):
    """This function defines the refund order item route"""
    order_item = OrderItem.query.get_or_404(orderitemid)
    order_item.refund()
    db.session.commit()
    flash('The order item has been refunded.', 'success')
    return redirect(url_for('orders.order', orderid=orderid))

@orders.route('/orders/<int:orderid>/refund', methods=['POST'])
@login_required
def refund_order(orderid):
    """This function defines the refund order route"""
    order = Order.query.get_or_404(orderid)
    order.refund()
    db.session.commit()
    flash('The order has been refunded.', 'success')
    return redirect(url_for('orders.orders'))

@orders.route('/orders/<int:orderid>/order_items/<int:orderitemid>/cancel', methods=['POST'])
@login_required
def cancel_order_item(orderid, orderitemid):
    """This function defines the cancel order item route"""
    order_item = OrderItem.query.get_or_404(orderitemid)
    order_item.cancel()
    db.session.commit()
    flash('The order item has been cancelled.', 'success')
    return redirect(url_for('orders.order', orderid=orderid))

@orders.route('/orders/<int:orderid>/cancel', methods=['POST'])
@login_required
def cancel_order(orderid):
    """This function defines the cancel order route"""
    order = Order.query.get_or_404(orderid)
    order.cancel()
    db.session.commit()
    flash('The order has been cancelled.', 'success')
    return redirect(url_for('orders.orders'))

@orders.route('/orders/<int:orderid>/order_items/<int:orderitemid>/complete', methods=['POST'])
@login_required
def complete_order_item(orderid, orderitemid):
    """This function defines the complete order item route"""
    order_item = OrderItem.query.get_or_404(orderitemid)
    order_item.complete()
    db.session.commit()
    flash('The order item has been completed.', 'success')
    return redirect(url_for('orders.order', orderid=orderid))

@orders.route('/orders/<int:orderid>/complete', methods=['POST'])
@login_required
def complete_order(orderid):
    """This function defines the complete order route"""
    order = Order.query.get_or_404(orderid)
    order.complete()
    db.session.commit()
    flash('The order has been completed.', 'success')
    return redirect(url_for('orders.orders'))

@orders.route('/transactions', methods=['GET', 'POST'])
@login_required
def transactions():
    """This function defines the transactions route"""
    transactions = Transaction.query.all()
    return render_template('transactions.html', title='Transactions', transactions=transactions)