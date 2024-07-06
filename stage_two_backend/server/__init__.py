#!/usr/bin/python3
"""
create the app instance
Initialize web application
"""

import os
import secrets
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager


HNG_MYSQL_HOST = os.environ.get('HNG_MYSQL_HOST')
HNG_MYSQL_DB = os.environ.get('HNG_MYSQL_DB')
HNG_MYSQL_USER = os.environ.get('HNG_MYSQL_USER')
HNG_MYSQL_PWD = os.environ.get('HNG_MYSQL_PWD')
HNG_MYSQL_ENV = os.environ.get('HNG_MYSQL_ENV')


app = Flask(__name__)


app.config['SECRET_KEY'] = secrets.token_hex()
app.config["JWT_SECRET_KEY"] = secrets.token.hex()
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{HNG_MYSQL_USER}:{HNG_MYSQL_PWD}@{HNG_MYSQL_HOST}:3306/{HNG_MYSQL_DB}'


db = SQLAlchemy(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
