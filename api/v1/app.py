#!/usr/bin/python3
"""Create and starts a Flaks application"""
from flask import Flask, Blueprint, render_template, abort
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)
print(app.url_map)

@app.teardown_appcontext
def close_database():
    """closes database session"""
    storage.close()

if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", 5000)
    app.run(host, port, threaded=True, debug=True)