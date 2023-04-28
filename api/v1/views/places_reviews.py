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
        all_places = models.storage.get(Place, place_id)
        if not all_places:
            abort(404)
        for reviews in all_places.reviews:
            return reviews.to_dict()

    if request.method == 'POST':
        placeObj = models.storage.get(Place, place_id)
        if not placeObj:
            abort(404)
        try:
            body = request.get_json()
        except Exception as e:
            abort(400, "Not a JSON")
        if body.get("user_id") is None:
            abort(400, "MIssing user_id")
        userObj = models.storage.get(User, body["user_id"])
        if not userObj:
            abort(404)
        if "text" not in body:
            abort(400, "Missing text")
        body["place_id"] = place_id
        newObj = Review(**body)
        models.storage.new(newObj)
        models.storage.save()
        return newObj.to_dict(), 201


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
    if request.method == 'GET':
        review = models.storage.get(Review, review_id)
        if review:
            return review.to_dict()
        abort(404)
    if request.method == 'PUT':
        reviewObj = models.storage.get(Review, review_id)
        if not reviewObj:
            abort(404)
        try:
            body = request.get_json()
        except Exception as e:
            abort(400, "Not a JSON")
        for key, val in body.items():
            if key not in ["id", "place_id", "created_at", "updated_at"]:
                setattr(review, key, val)
        models.storage.save()
        return reviewObj.to_dict()
