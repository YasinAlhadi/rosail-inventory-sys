#!/usr/bin/python3
"""This module contains the classes for the database"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from inventory.models.product import Product
from inventory.models.user import User
from inventory import db
from uuid import uuid4


class OrderItem(db.Model):
    """This class defines an order item by various attributes"""
    __tablename__ = 'order_item'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    productid = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    grandtotal = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    product = relationship(Product, backref='order_item', lazy=True)

    def __repr__(self):
        return f'OrderItem({self.id}, {self.orderid}, {self.productid}' \
                f', {self.quantity}, {self.subtotal}, {self.discount}' \
                f', {self.grandtotal})'
    
    def get_order_items(self, orderitemid):
        """This function gets an order item by id"""
        order_items = OrderItem.query.filter_by(orderid=orderitemid).all()
        return order_items
    
    def get_total(self, orderid):
        """This function gets the total of an order"""
        order_items = OrderItem.query.filter_by(orderid=orderid).all()
        total = 0
        for order_item in order_items:
            total += order_item.grandtotal
        return total

class Order(db.Model):
        """This class defines an order by various attributes"""
        __tablename__ = 'orders'
        id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
        order_number = Column(Integer, nullable=False, unique=True, autoincrement=True, default=1)
        userid = Column(Integer, ForeignKey('users.id'), nullable=False)
        order_itemid = Column(Integer, ForeignKey('order_item.id'), nullable=False)
        total = Column(Float, nullable=False)
        created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
        updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)
        user = relationship(User, backref='orders', lazy=True)
        order_item = relationship(OrderItem, backref='orders', lazy=True)

        def __repr__(self):
            return f'Order({self.id}, {self.userid}, {self.total})'
        
class Transaction(db.Model):
    """This class defines a transaction by various attributes"""
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    transactionid = Column(String(36), nullable=False, default=str(uuid4))
    orderid = Column(Integer, ForeignKey('orders.id'), nullable=False)
    amount = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    order = relationship(Order, backref='transactions', lazy=True)

    def __repr__(self):
        return f'Transaction({self.id}, {self.orderid}, {self.transactionid}' \
                f', {self.amount})'

        
db.create_all()