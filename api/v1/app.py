#!/usr/bin/python3
"""Create and starts a Flaks application"""
from flask import Flask, Blueprint, render_template, abort
from models import storage
from api.v1.views import app_views
import os
from flask import jsonify, make_response
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_database(close_db):
    """closes database session"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """displays a 404 if it does not match any route"""
    display_404 = jsonify({"error": "Not found"}), 404
    return make_response(display_404)


if __name__ == "__main__":
    api_host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    api_port = os.environ.get('HBNB_API_PORT', 5000)
    app.run(host=str(api_host), port=int(api_port), threaded=True, debug=True)
