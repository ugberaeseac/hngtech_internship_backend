#!/usr/bin/python3
"""
endpoint route to authenticate a user
Authenticates a user and creates a JWT token
if successful, returns the user id and access token else
displays an incorrect username/password message
"""

from server import app, db, bcrypt
from server.models import User
from flask import request, jsonify
from flask_jwt_extended import create_access_token


@app.route('/auth/login', methods=['POST'], strict_slashes=False)
def login():
    """
    authenticates and log in an authorized user
    """
    data - request.get_json()
    errors = []

    email = data['email']
    if not email:
        errors.append({'field': 'email', 'message': 'Please enter an email address'})
    password = data['password']
    if not password:
        errors.append({'field': 'password', 'message': 'Please enter a password'})

    if errors:
        return jsonify({'errors': errors}), 422

    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.userId)
    	return jsonify({
            'status': 'success',
            'message': 'Login successful',
            'data': {
                'accessToken': access_token,
                'user': {
                    'userId': user.userId,
                    'firstName': user.firstName,
                    'lastName': user.lastName,
                    'email': user.email,
                    'phone': user.phone,
                    }
                }
            }), 201
    else:
        return jsonify({
            'status': 'Bad request',
            'message': 'Authentication failed',
            'statusCode': 401
            }), 401

