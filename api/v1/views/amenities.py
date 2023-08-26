#!/usr/bin/python3
""" Module to handle all default RESTFul API actions """
from api.v1.views import app_views
from flask import jsonify, abort, request
import models
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """ Retrieves the list of all Amenity objects """
    all_amenities_list = []
    all_amenities = storage.all('Amenity')
    for amenity in all_amenities.values():
        all_amenities_list.append(amenity.to_dict())
    return jsonify(all_amenities_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """ Retrieves an Amenity by its id """
    all_amenities = storage.all('Amenity')
    key_to_find = str(Amenity.__name__) + '.' + amenity_id
    if key_to_find in all_amenities.keys():
        return jsonify(all_amenities.get(key_to_find).to_dict())
    else:
        abort(404)


@app_views.route(
    '/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity_by_id(amenity_id):
    """ Deletes an Amenity by its id """
    amenity_to_delete = storage.get(Amenity, amenity_id)
    if amenity_to_delete is None:
        abort(404)
    storage.delete(amenity_to_delete)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenitiess', methods=['POST'], strict_slashes=False)
def create_amenity():
    """ Creates an Amenity """
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.get_json()
    else:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    new_amenity = Amenity(**data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenites/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """Updates an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
