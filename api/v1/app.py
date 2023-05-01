#!/usr/bin/python3
"""Create and starts a Flaks application"""
from flask import Flask, Blueprint, render_template, abort
from models import storage
from api.v1.views import app_views
from os import getenv
from flask import jsonify, make_response
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})
print(app.url_map)

@app.teardown_appcontext
def close_database(close_db):
    """closes database session"""
    storage.close()

@app.errorhandler(404)
def page_not_found(error):
    """displays a 404 if it does not match any route"""
    display_404 = jsonify({"error": "Not found"})
    return make_response(display_404)


if __name__ == "__main__":
    api_host = getenv("HBNB_API_HOST", "0.0.0.0")
    api_port = getenv("HBNB_API_PORT", 5000)
    app.run(host=api_host, port=api_port, threaded=True, debug=True)