#!/usr/bin/python3
""" Returns the status of API """
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', methods=['GET'])
def status():
    """returst status:OK in json"""
    return jsonify({"status": "OK"})
