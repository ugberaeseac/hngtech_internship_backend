#!/usr/bin/python3
"""
API endpoint route to authenticate a user
Authenticates a user and creates a JWT token
if successful, returns the user id and access token else
displays an incorrect username/password message
"""

from server import db, bcrypt
from server.models.user import User
from server.models.organisation import Organisation
from server.views import app_views
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity


@app_views.route('/users/<id>', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_user(id):
    """
    Gets a user record
    protected route: user must be authenticated
    """
    if not id:
        return jsonify({
            'status': 'Bad request',
            'message': 'Please include the user id',
            'statusCode': 401
            }), 401

    current_user_id = get_jwt_identity()

    user = User.query.filter_by(userId=current_user_id).first() 
    if not user or current_user_id != id:
        return jsonify({
            'status': 'Bad request',
            'message': 'User not found',
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


@app_views.route('/organisations', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_organisation():
    """
    Gets the organisation(s) a user belongs to
    protected route: user must be authenticated
    """
    current_user_id = get_jwt_identity()
    
    user = User.query.filter_by(userId=current_user_id).first()
    if not user:
        return jsonify({
            'status': 'Forbidden',
            'message': 'Access denied',
            'statusCode': 401
            }), 401


    organisation_data = []
    for organisation in user.organisations:
        org_datum = {
                'OrgId': organisation.orgId,
                'name': organisation.name,
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


@app_views.route('/organisations/<orgId>', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_organisation_by_id(orgId):
    """
    Get an organisation by the orgId
    user must be authenticated
    """
    current_user_id = get_jwt_identity()

    organisation = Organisation.query.filter_by(orgId=orgId).first()
    if not organisation:
        return jsonify({
            'status': 'Bad request',
            'message': 'Organisation not found',
            'statusCode': 401
            }), 401
    
    user = User.query.filter_by(userId=current_user_id).first()
    if user:
        for orgs in user.organisations:
            if orgId == orgs.orgId:
                return jsonify ({
                    'status': 'success',
                    'message': 'API request successful',
                    'data': {
                        'orgId': orgs.orgId,
                        'name': orgs.name,
                        'description': orgs.description
                        }
                    }), 201
    else:
        return jsonify({
            'status': 'Forbidden',
            'message': 'Access denied',
            'statusCode': 401
            }), 401


@app_views.route('/organisations', methods=['POST'], strict_slashes=False)
@jwt_required()
def create_organisation():
    """
    create an organisation
    protected route: user must be authenticated
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()
    errors = []

    org_description = data['description']
    org_name = data['name']
    if not org_name:
        errors.append({'field': 'name', 'message': 'Please enter the name of the organisation'})

    if errors:
        return jsonify({'errors': errors}), 422

    new_organisation = Organisation(name=org_name, description=org_description)

    user = User.query.filter_by(userId=current_user_id).first()
    if user:
        new_organisation.users.append(user)
        db.session.add(new_organisation)
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': 'Organisation created successfully',
            'data': {
                'orgId': new_organisation.orgId,
                'name': new_organisation.name,
                'description': new_organisation.description
                }
            }), 201
    else:
        return jsonify({
            'status': 'Bad request',
            'message': 'Client error',
            'statusCode': 400
            }), 400


@app_views.route('/organisations/<orgId>/users', methods=['POST'], strict_slashes=False)
def add_user_to_organisation(orgId):
    """
    Adds a user to a organisation
    """
    data = request.get_json()
    errors = []

    user_id = data['userId']
    if not user_id:
        errors.append({'field': 'userId', 'message': 'Please enter the user id'})

    if errors:
        return jsonify({'errors': errors}), 422

    organisation = Organisation.query.filter_by(orgId=orgId).first()
    if not organisation:
        return jsonify({
            'status': 'Bad request',
            'message': 'Organisation not found',
            'statusCode': 401
            }), 401

    user = User.query.filter_by(userId=user_id).first()
    if not user:
        return jsonify({
            'status': 'Bad request',
            'message': 'User not found',
            'statusCode': 401
            }), 401
    
    if user in user.organisations:
        return jsonify({
            'status': 'Bad request',
            'message': 'User is already in this organisation',
            'statusCode': 401
            }), 401

    organisation.users.append(user)
    db.session.commit()

    return jsonify({
        'status': 'success',
        'message': 'User added to organisation successfully'
        }), 201




