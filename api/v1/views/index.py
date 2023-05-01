#!/usr/bin/python3
"""module for index.py"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False, methods=["GET"])
def status():
    """returns the status of this route"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False, methods=["GET"])
def stats():
    """
    an endpoint or route that retrieves
    the number of each objects by type
    """
    item_class = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(item_class)
