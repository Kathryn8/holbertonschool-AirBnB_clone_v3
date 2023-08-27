#!/usr/bin/python3
'''
This module contains the view for restful api of the
city obj.
'''

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_places_reviews(place_id):
    '''
    Gets all reviews linked to place id. Raises 404 error if
    place_id is not linked to place obj.
    '''
    review_list = []
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)
    for review in place_obj.reviews:
        review_list.append(review.to_dict())

    return jsonify(review_list)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_one_review(review_id):
    '''
    Gets one review obj, if none found raises 404.
    '''
    review_obj = storage.get(Review, review_id)

    if review_obj is None:
        abort(404)

    return jsonify(review_obj.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    '''
    Checks to see if review exists before deleting.
    Returns 404 on error.
    200 on success.
    '''
    review_obj = storage.get(Review, review_id)
    if review_obj is None:
        abort(404)

    storage.delete(review_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'],
                 strict_slashes=False)
def create_new_place_review(place_id):
    '''
    Function creates a new review with the place id.
    Checks to see if http body is good json else returns 400
    if place_id doesn't exist returns 404.
    if json body doesn't contain name key returns 400
    Returns 201 on success.
    '''
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)

    new_obj = request.get_json(silent=True)
    if new_obj is None:
        abort(400, 'Not a Json')

    if new_obj.get('name') is None:
        abort(400, 'Missing name')

    if new_obj.get('user_id') is None:
        abort(400, 'Missing user_id')

    if new_obj.get('text') is None:
        abort(400, 'Missing text')

    user_obj = storage.get(User, new_obj.get('user_id'))
    if user_obj is None:
        abort(404)

    new_obj.update({'place_id': place_id})

    new_review = Review(**new_obj)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    '''
    Updates a review by review_id with the http body response.
    Checks to see if reivew exists, else returns 404.
    Checks to see if response body is JSON or returns 400.
    On success return review obj and 201.
    '''
    review_obj = storage.get(Review, review_id)
    if review_obj is None:
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
            setattr(review_obj, key, value)
    storage.save()
    return jsonify(review_obj.to_dict()), 200
