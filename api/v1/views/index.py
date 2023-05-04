#!/usr/bin/python3
"""create a blueprint for views"""
from models.user import User
from models.state import State
from models.review import Review
from models.place import Place
from models.city import City
from models.base_model import BaseModel
from models.amenity import Amenity
import models
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def get_status():
    """return the status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def get_stats():
    """Get the db stats"""
    classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
               "Place": Place, "Review": Review, "State": State, "User": User}
    objects = {}
    objects['amenities'] = models.storage.count(Amenity)
    objects['cities'] = models.storage.count(City)
    objects['places'] = models.storage.count(Place)
    objects['reviews'] = models.storage.count(Review)
    objects['states'] = models.storage.count(State)
    objects['users'] = models.storage.count(User)
    return jsonify(objects)
