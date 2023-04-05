#!/usr/bin/python3
"""This module contains initailization for the inventory package"""
import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://rms_admin:rms1516@localhost/rms_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)





from inventory.users.routes import users
from inventory.main.routes import main
from inventory.products.routes import prod
from inventory.orders.routes import ord

app.register_blueprint(users)
app.register_blueprint(main)
app.register_blueprint(prod)
app.register_blueprint(ord)