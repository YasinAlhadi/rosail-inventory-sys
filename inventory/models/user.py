#!/usr/bin/python3
"""This module contains the classes for the database"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from flask_login import UserMixin
from inventory import db, app, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """This class defines a user by various attributes"""
    __searchble__ = ['name', 'email']
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    roleid = Column(Integer, nullable=False)
    name = Column(String(128), nullable=False)
    phone = Column(String(128), nullable=False)
    address = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'User({self.name}, {self.email})'


db.create_all()
