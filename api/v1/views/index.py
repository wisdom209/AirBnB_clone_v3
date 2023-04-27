#!/usr/bin/python3
"""create a blueprint for views"""
from flask import jsonify, Blueprint
app_views = Blueprint('app_views_blueprint', __name__, url_prefix='/api/v1')


@app_views.route('/status', strict_slashes=False)
def get_status():
    """return the status"""
    return jsonify({"status": "Ok"})


@app_views.route('/stats', strict_slashes=False)
def get_stats():
    """Get the db stats"""
    import models
    objects = {}
    key_set = set()
    all = models.storage.all()
    for key in all.keys():
        key_set.add(key.split('.')[0])
    for key in key_set:
        count = 0
        for keyObj in all.keys():
            if keyObj.startswith(key):
                count += 1
        objects[key] = count
    return jsonify(objects)
