#!/usr/bin/python3
"""
API endpoint route to authenticate a user
Authenticates a user and creates a JWT token
if successful, returns the user id and access token else
displays an incorrect username/password message
"""

from server import db, bcrypt
from server.models import User
from server.views import app_views
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity


@app_views.route('/users/<id>', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_user(user_id):
    """
    Gets a user record
    """
    if not user_id:
        return jsonify({
            'status': 'Bad request',
            'message': 'Please include the user id',
            'statusCode': 401
            }), 401

    current_user_id = get_jwt_identity()

    user = User.query.filter_by(userId=current_user_id).first() 
    if not user or current_user_id != user_id:
        return jsonify({
            'status': 'Bad request',
            'message': 'User not found',
            'statusCode': 401
            }), 401

    if current_user_id != user_id:
        return jsonify({
            'status': 'Bad request',
            'message': 'Access denied',
            'statusCode': 401
            }), 401

    return jsonify({
        'status': 'success',
        'message': 'API request successful',
        'data': {
            'userId': user.userId,
            'firstName': user.firstName,
            'lastName': user.lastName,
            'email': user.email,
            'phone': user.phone
            }
        }), 200


@app_views.route('/organisations', methods=[], strict_slashes=False)
@jwt_required()
def get_organisation():
    """
    Gets the organisation(s) a user belongs to
    """
    current_user_id = get_jwt_identity()
    
    user = User.query.filter_by(userId=current_user_id).first()
    if not user:
        return jsonify({
            'status': 'Bad request',
            'message': 'Access denied',
            'statusCode': 401
            }), 401

    organisation_data = []
    for organisation in user.organisations:
        org_datum = {
                'OrgId': organisation.orgId
                'name': organisation.name
                'description': organisation.description
                }
    organisation_data.append(org_datum)
    
    return jsonify({
        'status': 'success',
        'message': 'API request was successful',
        'data': {
            'organisations': organisation_data
            }

        }), 200





