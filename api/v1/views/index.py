#!/usr/bin/python3
"""module for index.py"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """returns the status of this route"""
    jsonify({"status": "OK"})