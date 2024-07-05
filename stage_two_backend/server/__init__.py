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



HNG_MYSQL_HOST = os.environ.get('HNG_MYSQL_HOST')
HNG_MYSQL_DB = os.environ.get('HNG_MYSQL_DB')
HNG_MYSQL_USER = os.environ.get('HNG_MYSQL_USER')
HNG_MYSQL_PWD = os.environ.get('HNG_MYSQL_PWD')
HNG_MYSQL_ENV = os.environ.get('HNG_MYSQL_ENV')


app = Flask(__name__)
bcrypt = Bcrypt(app)


app.config['SECRET_KEY'] = secrets.token_hex()
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{HNG_MYSQL_USER}:{HNG_MYSQL_PWD}@{HNG_MYSQL_HOST}:3306/{HNG_MYSQL_DB}'
db = SQLAlchemy(app)
