#!/usr/bin/python3
"""Starting up a Flask app"""
from models import storage
from models import *
import os

from api.v1.views import app_views
from flask import Flask, jsonify
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(excepts):
    """remove session"""
    storage.close()


if __name__ == '__main__':
    port = os.getenv("HBNB_API_PORT") if os.getenv(
        "HBNB_API_PORT") else '5000'
    host = os.getenv("HBNB_API_HOST") if os.getenv(
        "HBNB_API_HOST") else '0.0.0.0'
    app.run(port=port, host=host, debug=True, threaded=True)
