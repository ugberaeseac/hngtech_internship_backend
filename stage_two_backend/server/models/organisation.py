#!/usr/bin/python3
"""
Model for the organisation table
Maps tables to python classes and prints
the string representation of the class
"""


import uuid
from server import db
from server.models import User


user_organisations = db.Table('user_orginisations',
        db.Column('user_id', UUID(as_uuid=True), db.ForeignKey('user.userId'), primary_key=True),
        db.Column('organisation_id', UUID(as_uuid=True), db.ForeignKey('organisation.orgId'), primary_key=True):w:wi
        )


class Organisation(db.Model):
    """
    creates a Organisation class which maps
    to the organisation table
    """
    __tablename__ == 'organisation'
    orgId = db.Column(UUID(as_uuid=True, primary_key=True, default=uuid.uuid4, unique=True))
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(120))
    
    def __repr__(self):
        """
        Prints the custom string representation of the Organisation class
        """
        return f'Organisation({self.orgId}, {self.name}, {self.description})'

