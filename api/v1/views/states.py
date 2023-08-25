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


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """ Retrieves the list of all State objects """
    all_states_list = []
    all_states = storage.all('State')
    for _state in all_states.values():
        all_states_list.append(_state.to_dict())
    return jsonify(all_states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id):
    """ Retrieves a State by its id """
    all_states = storage.all('State')
    key_to_find = str(State.__name__) + '.' + state_id
    if key_to_find in all_states.keys():
        return jsonify(all_states.get(key_to_find).to_dict())
    else:
        abort(404)


@app_views.route(
    '/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state_by_id(state_id):
    """ Deletes a State by its id """
    state_to_delete = storage.get(State, state_id)
    if state_to_delete is None:
        abort(404)
    storage.delete(state_to_delete)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_states():
    """ Creates a state """
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.get_json()
    else:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
