#!/usr/bin/python3
"""
displays the Home page
"""

from server import app

@app.route('/', methods=['GET'], strict_slashes=False)
def home():
    """
    Index page
    """
    return ('<h1> Home Page </h1>')
