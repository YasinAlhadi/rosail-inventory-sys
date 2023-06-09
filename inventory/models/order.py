#!/usr/bin/python3
"""This module stores the oders"""
from datetime import datetime
from inventory import db
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from inventory.models.user import User
import json


class JsonDict(db.TypeDecorator):
    """Class"""
    impl = db.Text

    def process_bind_param(self, value, dialect):
        """Process"""
        if value is None:
            return '{}'
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        """Process"""
        if value is None:
            return {}
        return json.loads(value)


class Orders(db.Model):
    """This class defines table that stores the orders"""
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    invoice_number = Column(String(100), nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'),
                     unique=False, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    order = Column(JsonDict, nullable=False)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    user = relationship('User', backref='orders')

    def __repr__(self):
        """This function returns the order"""
        return f"Order('{self.invoice_number}', '{self.user_id}', '{self.created_at}')"


db.create_all()
