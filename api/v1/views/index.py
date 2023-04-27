#!/usr/bin/python3
"""create a blueprint for views"""
from flask import jsonify, Blueprint
app_views = Blueprint('app_views_blueprint', __name__, url_prefix='/api/v1')


@app_views.route('/status', strict_slashes=False)
def get_status():
    """return the status"""
    return jsonify({"status": "Ok"})
