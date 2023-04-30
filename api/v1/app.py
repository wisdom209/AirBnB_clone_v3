#!/usr/bin/python3
"""Starting up a Flask app"""
from models import storage
from models import *
import os

from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.errorhandler(404)
def error_page(error):
    """error 404 page"""
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def tear_down(excepts):
    """remove session"""
    storage.close()


if __name__ == '__main__':
    port = os.getenv("HBNB_API_PORT") if os.getenv(
        "HBNB_API_PORT") else '5000'
    host = os.getenv("HBNB_API_HOST") if os.getenv(
        "HBNB_API_HOST") else '0.0.0.0'
    app.run(port=port, host=host, threaded=True, debug=True)
