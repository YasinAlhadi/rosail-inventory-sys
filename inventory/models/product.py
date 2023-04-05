#!/usr/bin/python3
"""This module contains the classes for the database"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from inventory import db

class Product(db.Model):
    """This class defines a product by various attributes"""
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(128), nullable=False)
    description = Column(String(128), nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    brand_id = Column(Integer, ForeignKey('brands.id'), nullable=False)
    brand = relationship('Brand', backref='products')
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    category = relationship('Category', backref='products')

    def __repr__(self):
        return f'Product({self.name}, {self.description}, {self.price}, {self.quantity}, {self.category_id})'

class Category(db.Model):
    """This class defines a category by various attributes"""
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(128), nullable=False)
    description = Column(String(128), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'Category({self.name}, {self.description})'

class Brand(db.Model):
    """This class defines a brand by various attributes"""
    __tablename__ = 'brands'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(128), nullable=False)
    description = Column(String(128), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'Brand({self.name}, {self.description})'

db.create_all()