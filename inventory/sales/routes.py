#!/usr/bin/python3
"""This module contains the sales routes"""
from flask import Blueprint, render_template, url_for, flash, redirect, request, session
from sqlalchemy import func
from inventory.models.order import Orders
from inventory import db
from flask_login import login_required, current_user
from datetime import datetime
from datetime import date

sal = Blueprint('sales', __name__)


@sal.route('/sales')
@login_required
def sales():
    """This function shwos the sales"""
    user = current_user
    total_sales = db.session.query(db.func.sum(Orders.total_price)).filter(
        func.DATE(Orders.created_at) == datetime.today().date()).all()
    return render_template('sales.html', title='Sales', user=user, total_sales=total_sales)
