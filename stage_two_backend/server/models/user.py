#!/usr/bin/python3
"""
Model for the users table
Maps tables to python classes and prints
the string representation of the class
"""

import uuid
from server import db


user_organisations = db.Table('user_organisations',
        db.Column('user_id', db.String(120), db.ForeignKey('users.userId'), primary_key=True),
        db.Column('organisation_id', db.String(120), db.ForeignKey('organisations.orgId'), primary_key=True))

class User(db.Model):
    """
    creates a User class which maps to the users table
    """
    __tablename__ = 'users'
    userId = db.Column(db.String(120), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    firstName = db.Column(db.String(60), nullable=False)
    lastName = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))

    organisations = db.relationship('Organisation', secondary='user_organisations', backref='users') 
    
    def __repr__(self):
        """
        Prints the custom string representation of the User class
        """
        return f'User({self.userId}, {self.firstName} {self.lastName}, {self.email}, {self.phone}'



