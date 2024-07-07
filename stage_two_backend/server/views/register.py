#!/usr/bin/python3
"""
endpoint route for registration/signup
creates a new user
return payload if success else error
"""

from server import app, db, bcrypt
from server.models.user import User
from server.models.organisation import Organisation
from flask import request, jsonify
from flask_jwt_extended import create_access_token


@app.route('/auth/register', methods=['POST'], strict_slashes=False)
def register():
    """
    creates a new user
    returns payload if successful
    """
    data = request.get_json()
    errors = []

    firstname = data['firstName']
    if not firstname:
        errors.append({'field': 'firstName', 'message': 'Please provide the firstName field'})
    lastname = data['lastName']
    if not lastname:
        errors.append({'field': 'lastName', 'message': 'Please provide the lastName field'})
    email = data['email']
    if not email:
        errors.append({'field': 'email', 'message': 'Please provide the email field'})
    password = data['password']
    if not password:
        errors.append({'field': 'password', 'message': 'Please provide a password'})
    phone = data['phone']
    if not phone:
        errors.append({'field': 'phone', 'message': 'Please enter a phone number'})

    if errors:
        return jsonify({'errors': errors}), 422

    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({
            'status': 'Bad request',
            'message': 'Registration unsuccessful',
            'statusCode': 400
            }), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(firstName=firstname,
                    lastName=lastname,
                    email=email,
                    password=hashed_password,
                    phone=phone
                    )
    organisation_name =f'{firstname}\'s organisation'
    new_organisation = Organisation(name=organisation_name,
                                    description=f'This is the description of {organisation_name}'
                    )
    new_user.organisations.append(new_organisation)

    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=new_user.userId)

    return jsonify({
        'status': 'success',
        'message': 'Registration successful',
        'data': {
        'accessToken': access_token,
        'user': {
    	'userId': new_user.userId,
	    'firstName': new_user.firstName,
    	'lastName': new_user.lastName,
	    'email': new_user.email,
		'phone': new_user.phone,
        }
    }
    }), 201

