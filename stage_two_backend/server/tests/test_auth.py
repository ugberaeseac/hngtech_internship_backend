#!/usr/bin/python3
"""
Unittest
"""

import unittest
from datetime import datetime, timedelta
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token, decode_token
from server.models.user import User
from server.models.organisation import Organisation


class TestTokenGeneration(unittest.TestCase):
    """
    Test for token generation
    """

    def test_token_expiration(self):
        with app.app_context():
            token = create_access_token(identity="test_user")
            decoded_token = decode_token(token)
        
            # Ensure token expires in 15 minutes
            expiration_time = datetime.fromtimestamp(decoded_token['exp'])
            expected_expiration = datetime.utcnow() + timedelta(minutes=15)
        
            self.assertLessEqual(expected_expiration, expiration_time)

    def test_token_user_details(self):
        user_id = "test_user"
        token = create_access_token(identity=user_id)
        decoded_token = decode_token(token)
        
        self.assertEqual(decoded_token['sub'], user_id)



class TestOrganisationAccess(unittest.TestCase):
    """
    Test for authorized and unathorized organisation access
    """

    def setUp(self):
        # Setup Flask app and database
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///unittest.db'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['SECRET_KEY'] = '99282c8533e510478f3a02d1738f313aef56002f5bd965619db670c8cc9640cc'
        self.app.config['JWT_SECRET_KEY'] = 'a62bf96415e294f8f7903537f509a471ad4cdd57ed70844dd0adb8f38729f761'
        
        self.db = SQLAlchemy(self.app)
        self.jwt = JWTManager(self.app)

        # Create test client
        self.client = self.app.test_client()

    def tearDown(self):
        # Clean up database sessions and connections
        with self.app.app_context():
            self.db.session.remove()
            self.db.drop_all()

    def test_organisation_access_restriction(self):
        # Create test data: user, organisations
        with self.app.app_context():
            user = User(firstName='John', lastName='Doe', email='john.doe@example.com', password='securepassword', phone='1234567890')
            organisation1 = Organisation(name="John's Organisation", description="Description")
            organisation2 = Organisation(name="Other's Organisation", description="Description")
            
            user.organisations.append(organisation1)
            self.db.session.add(user)
            self.db.session.commit()

            # Simulate login
            access_token = create_access_token(identity=user.userId)
            
            # Access organisation data
            response = self.client.get(f'/api/organisations/{organisation1.orgId}', headers={'Authorization': f'Bearer {access_token}'})
            self.assertEqual(response.status_code, 200)
            
            # Attempt to access unauthorised organisation data
            response = self.client.get(f'/api/organisations/{organisation2.orgId}', headers={'Authorization': f'Bearer {access_token}'})
            self.assertEqual(response.status_code, 403)

if __name__ == '__main__':
    unittest.main()
