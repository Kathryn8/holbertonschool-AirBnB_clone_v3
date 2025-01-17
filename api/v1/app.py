#!/usr/bin/python3
"""A script that starts a Flask web application"""
from flask import Flask
from flask import jsonify
from models import storage
from api.v1.views import app_views
from os import environ
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, origins='0.0.0.0')


@app.teardown_appcontext
def teardown_db(exception):
    """ remove the current SQLAlchemy Session"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    HBNB_API_HOST = environ.get('HBNB_API_HOST', '0.0.0.0')
    HBNB_API_PORT = environ.get('HBNB_API_PORT', 5000)
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
