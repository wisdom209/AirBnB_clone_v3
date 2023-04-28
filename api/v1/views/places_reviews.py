#!/usr/bin/python3
"""Handle state objects"""
from ast import mod
import re
from models.user import User
from models.state import State
from models.review import Review
from models.place import Place
from models.city import City
from models.base_model import BaseModel
from models.amenity import Amenity
import models
import datetime
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
def work_on_all_reviews_by_place_id(place_id):
    """retrieve the state's cities"""
    if request.method == 'GET':
        place_obj = models.storage.get(classes['Place'], place_id)
        if not place_obj:
            abort(404)
        place_list = []
        all_places = models.storage.all(classes["Place"])
        for value in all_places.values():
            place_id.append(value.to_dict())
        return place_list


@app_views.route('/reviews/<review_id>', methods=['GET', 'POST', 'DELETE'],
                 strict_slashes=False)
def work_on_a_review(review_id):
    """working on a review"""
    if request.method == 'DELETE':
        review_obj = models.storage.get(classes['Review'], review_id)
        if not review_obj:
            abort(404)
        models.storage.delete(review_obj)
        models.storage.save()
        return {}
