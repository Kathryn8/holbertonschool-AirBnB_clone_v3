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


@app_views.route(
    '/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_all_cities_by_state(state_id):
    """ Retrieves the list of all City objects belonging to a state """
    state_to_match = storage.get(State, state_id)
    if state_to_match is None:
        abort(404)
    new_list_of_cities = []
    all_cities = storage.all('City')
    for object in all_cities.values():
        if state_id == object.state_id:
            new_list_of_cities.append(object.to_dict())
    return jsonify(new_list_of_cities)


@app_views.route(
    '/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_by_id(city_id):
    """ Retrieves a Citye by its id """
    city_object = storage.get(City, city_id)
    if city_object is None:
        abort(404)
    return jsonify(city_object.to_dict())


@app_views.route(
    '/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city_by_id(city_id):
    """ Deletes a City by its id """
    city_to_delete = storage.get(City, city_id)
    if not city_to_delete:
        abort(404)
    storage.delete(city_to_delete)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    '/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """ Creates a city """
    reference_state = storage.get(State, state_id)
    if not reference_state:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    new_city = City(**data)
    new_city.state_id = state_id
    reference_state.cities.append(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a City object"""
    city_to_update = storage.get(City, city_id)
    if not city_to_update:
        abort(404)
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city_to_update, key, value)
    city_to_update.save()
    return jsonify(city_to_update.to_dict()), 200
