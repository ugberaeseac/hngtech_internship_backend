#!/usr/bin/python3
"""
create the app instance
"""


from flask import Flask


app = Flask(__name__)

from route import *
