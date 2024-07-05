#!/usr/bin/python3
"""
Model for the users table
Maps tables to python classes and prints
the string representation of the class
"""

import uuid
from server import db


class User(db.Model):
    """
    creates a User class which maps to the users table
    """
    __tablename__ == 'users'
    userId = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    firstName = db.Column(db.String(60), nullabl=False)
    lastName = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))

    organisation = db.relationship('Organisation', secondary='user_org', backref='user', cascade='all delete-orphan') 
    
    def __repr__(self):
        """
        Prints the custom string representation of the User class
        """
        return f'User({self.userId}, {self.firstName} {self.lastName}, {self.email}, {self.phone}'

