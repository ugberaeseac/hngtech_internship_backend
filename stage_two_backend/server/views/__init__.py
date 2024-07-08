#!?usr/bin/python3
"""
Create a Blueprint
Import views for the endpoints
"""

from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api')


from server.views.home import *
from server.views.register import *
from server.views.login import *
from server.views.organisation import *
