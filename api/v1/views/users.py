#!/usr/bin/python3
'''
This module contains the view for the restful API for the
user obj.
'''

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'])
def get_all_users():
    '''
    Returns all users in the database.
    '''
    users_list = []
    all_users = storage.all('User')
    for user_obj in all_users.values():
        users_list.append(user_obj.to_dict())

    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_one_user(user_id):
    '''Returns the one user in json or else the 404 page.'''
    result = storage.get(User, user_id)
    if result is None:
        abort(404)

    user_obj = result.to_dict()
    return jsonify(user_obj)


@app_views.route('/users/<user_id>', methods=['Delete'])
def delete_one_user(user_id):
    '''Deletes the one user, raise 404 error if not found'''
    result = storage.get(User, user_id)
    if result is None:
        abort(404)

    storage.delete(result)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    '''Creates a new user from the http body'''
    new_obj = request.get_json()
    '''If not json abort to 400 code'''
    if new_obj is None:
        abort(400, 'Not a JSON')

    '''If obj doesn't have key of name, abort 400'''
    if new_obj.get('email') is None:
        abort(400, 'Missing email')
    '''If obj doesn't have key of password, abort 400'''
    if new_obj.get('password') is None:
        abort(400, 'Missing name')

    '''Create new obj, save to storage and return json obj.'''
    new_user = User(**new_obj)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    '''
    Updates user by id. Checks to make sure if it exists.
    Sends either 404 if states doesn't exists.
    Sends 400 if json in http body is bad.
    Ignores keys id, updated_at, created_at, email.
    '''
    new_attributes = request.get_json()
    if new_attributes is None:
        abort(400, 'Not a JSON')

    one_user = storage.get(User, user_id)
    if one_user is None:
        abort(404)

    skip_keys = ['id', 'created_at', 'updated_at', 'email']
    for key, value in new_attributes.items():
        if key in skip_keys:
            pass
        else:
            setattr(one_user, key, value)
    storage.save()
    return jsonify(one_user.to_dict()), 200
