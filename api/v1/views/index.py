#!/usr/bin/python3
"""create a blueprint for views"""
from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status')
def get_status():
    """return the status"""
    return jsonify({"status": "Ok"})
