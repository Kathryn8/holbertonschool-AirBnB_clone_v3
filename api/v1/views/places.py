#!/usr/bin/python3
'''
This module contains the view for the restful API for the
places obj.
'''

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    '''
    Returns all places associated with the city_id.
    Returns 404 if city not found.
    '''
    places_list = []
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)

    for place in city_obj.places:
        places_list.append(place.to_dict())

    return jsonify(places_list)


@app_views.route('/places/<place_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_one_place(place_id):
    '''
    Returns one place obj, 404 if the place_id is not
    associated with place_obj.
    '''
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)

    return jsonify(place_obj.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_one_place(place_id):
    '''
    Deletes one place obj, 404 if the place_id is not
    associated with place_obj.
    '''
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)

    storage.delete(place_obj)
    storage.save()

    return jsonify({}), 200


@app_views.route('cities/<city_id>/places',
                 methods=['POST'],
                 strict_slashes=False)
def create_new_place(city_id):
    '''
    Creates a new place associated with the city_id.
    Returns 404 if city_id doesn't exist in storage already.
    if http body doesn't contain valid JSON raise 400.
    if user_id is not dict raise a 400.
    if user_id is in storage raise a 404.
    If name is not in dict raise 400.
    Raise 200 on success.
    '''
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)

    new_obj = request.get_json()
    if new_obj is None:
        abort(400, 'Not a Json')

    if new_obj.get('name') is None:
        abort(400, 'Missing name')

    if new_obj.get('user_id') is None:
        abort(400, 'Missing user_id')

    user_obj = storage.get(User, new_obj.get('user_id'))
    if user_obj is None:
        abort(404)

    new_obj.update({'city_id': city_id})

    new_place = Place(**new_obj)
    storage.new(new_place)
    storage.save()

    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    '''
    Updates place obj if exists in storage.
    Returns 404 if place_id returns None.
    Skip id, user_id, city_id, created_at, updated_at.
    Return 200 on success.
    '''
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)

    new_attributes = request.get_json()
    if new_attributes is None:
        abort(400, 'Not a Json')

    skip_keys = ['id', 'created_at', 'updated_at',
                 'user_id', 'city_id']

    for key, value in new_attributes.items():
        if key in skip_keys:
            pass
        else:
            setattr(place_obj, key, value)
    storage.save()
    return jsonify(place_obj.to_dict()), 200
