#!/usr/bin/python3
'''
This module contains the view for restful api of the
city obj.
'''

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'])
def get_all_amenities():
    '''
    Returns the json object of all amenities in storage
    '''
    amenity_list = []
    all_amenities = storage.all('Amenity')
    for _amenity in all_amenities.values():
        amenity_list.append(_amenity.to_dict())

    return jsonify(amenity_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_one_amenity(amenity_id):
    '''
    Gets one amenity obj, if none found raises 404.
    '''
    result = storage.get(Amenity, amenity_id)
    if result is None:
        abort(404)

    single_amenity_dict = result.to_dict()
    return jsonify(single_amenity_dict)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    '''
    Checks to see if amenity exists before deleting.
    Returns 404 on error.
    200 on success.
    '''
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        abort(404)

    storage.delete(amenity_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    '''
    Creates a new amenity from the http body
    '''
    amenity_obj = request.get_json(silent=True)
    '''If not json, aborts to a 400 code with message'''
    if amenity_obj is None:
        abort(400, 'Not a JSON')

    '''If obj doesn't have a key of a name abort 400 with message'''
    if amenity_obj.get('name') is None:
        abort(400, 'Missing name')

    '''Create new obj, save to storage and return json object'''
    new_amenity = Amenity(**amenity_obj)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    '''
    Updates an amenity by amenity_id with the http body response.
    Sends either 404 if states doesn't exists.
    Sends 400 if json in http body is bad.
    Ignores keys id, updated_at, created_at.
    '''
    new_attributes = request.get_json()
    if new_attributes is None:
        abort(400, 'Not a Json')
    one_amenity = storage.get(Amenity, amenity_id)
    if one_amenity is None:
        abort(404)

    skip_keys = ['id', 'created_at', 'updated_at']
    for key, value in new_attributes.items():
        if key in skip_keys:
            pass
        else:
            setattr(one_amenity, key, value)
    storage.save()
    return (one_amenity.to_dict()), 200
