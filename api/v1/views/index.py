#!/usr/bin/python3
"""module for index.py"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=["GET"])
def status():
    """returns the status of this route"""
    return jsonify({"status": "OK"})