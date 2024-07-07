#!/usr/bin/python3
"""
Model for the organisation table
Maps tables to python classes and prints
the string representation of the class
"""


import uuid
from server import db
from server.models.user import User


class Organisation(db.Model):
    """
    creates a Organisation class which maps
    to the organisation table
    """
    __tablename__ = 'organisations'
    orgId = db.Column(db.String(120), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(120))
    
    def __repr__(self):
        """
        Prints the custom string representation of the Organisation class
        """
        return f'Organisation({self.orgId}, {self.name}, {self.description})'

