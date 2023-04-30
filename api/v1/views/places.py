#!/usr/bin/python3
"""Handle places objects"""
from ast import mod
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


@app_views.route('cities/<city_id>/places',
                 methods=['GET', 'POST'], strict_slashes=False)
def places_obj(city_id):
    """function that retrieves and create places"""
    if request.method == 'GET':
        cityObj = models.storage.get(City, city_id)
        if not cityObj:
            abort(404)
        for place in cityObj.places:
            return jsonify(place.to_dict())

    if request.method == 'POST':
        cityObj = models.storage.get(City, city_id)
        if not cityObj:
            abort(404)
        body = request.get_json()
        if not body:
            abort(400, "Not a JSON")
        body["city_id"] = city_id
        if "user_id" not in body:
            abort(400, "Missing user_id")
        userObj = models.storage.get(User, body["user_id"])
        if not userObj:
            abort(404)
        if "name" not in body:
            abort(400, "Missing name")
        newObj = Place(**body)
        """models.storage.new(newObj)"""
        newObj.save()
        return make_response(jsonify(newObj.to_dict()), 201)


@app_views.route('/places/<place_id>',
                 methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def places_http_methods(place_id):
    """methods for GET, PUT, and DELETE using id variable"""
    if request.method == 'GET':
        placeNeeded = models.storage.get(Place, place_id)
        if placeNeeded:
            return jsonify(placeNeedeed.to_dict())
        abort(404)
    if request.method == 'DELETE':
        placeNeeded = models.storage.get(Place, place_id)
        if placeNeeded:
            models.storage.delete(placeNeeded)
            models.storage.save()
            return make_response(jsonify({}), 200)
        abort(404)
    if request.method == 'PUT':
        placeObj = models.storage.get(Place, place_id)
        if not placeObj:
            abort(404)
        body = request.get_json()
        if not body:
            abort(400, "Not a JSON")
        ignore = ["id", "user_id", "city_id", "created_at", "updated_at"]
        for key, val in body.items():
            if key not in ignore:
                setattr(placeObj, key, val)
        models.storage.save()
        return make_response(jsonify(placesObj.to_dict()), 200)
