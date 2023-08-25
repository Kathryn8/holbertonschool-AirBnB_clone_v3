#!/usr/bin/python3
""" Returns the status of API """
from api.v1.views import app_views
from flask import jsonify
import models
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

@app_views.route('/status', methods=['GET'])
def status():
    """returns status:OK in json"""
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'])
def stats():
    """retrieves the number of each objects by type"""
    cls = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}
    new_dict = {k: storage.count(v) for (k, v) in cls.items()}
    return jsonify(new_dict)
