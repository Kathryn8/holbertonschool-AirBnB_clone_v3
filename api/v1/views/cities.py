#!/usr/bin/python3
'''
This module contains the view for restful api of the
city obj.
'''

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_city_state(state_id):
    '''
    Gets all cities linked to state id. Raises 404 error if
    state_id is not linked to sstate obj.
    '''
    city_list = []
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    for city in state_obj.cities:
        city_list.append(city.to_dict())

    return jsonify(city_list)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_one_city(city_id):
    '''
    Gets one city obj, if none found raises 404.
    '''
    city_obj = storage.get(City, city_id)

    if city_obj is None:
        abort(404)

    return jsonify(city_obj.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    '''
    Checks to see if city exists before deleting.
    Returns 404 on error.
    200 on success.
    '''
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)

    storage.delete(city_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    '''
    Function creates a new city with the state id.
    Checks to see if http body is good json else returns 400
    if state_id doesn't exist returns 404.
    if json body doesn't contain name key returns 400
    Returns 201 on success.
    '''
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)

    new_obj = request.get_json()
    if new_obj is None:
        abort(400, 'Not a Json')

    if new_obj.get('name') is None:
        abort(400, 'Missing name')

    new_obj.update({'state_id': state_id})

    new_city = City(**new_obj)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    '''
    Updates a city by city_id with the http body response.
    Checks to see if city exists, else returns 404.
    Checks to see if response body is JSON or returns 400.
    On success return city obj and 201.
    '''
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)

    new_attributes = request.get_json()
    if new_attributes is None:
        abort(400, 'Not a Json')

    skip_keys = ['id', 'created_at', 'updated_at']
    for key, value in new_attributes.items():
        if key in skip_keys:
            pass
        else:
            setattr(city_obj, key, value)
    storage.save()
    return (city_obj.to_dict()), 200
