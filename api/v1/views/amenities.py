#!/usr/bin/python3
"""Handle amenities objects"""
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


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def amenity_obj():
    """function that retrieves and create amenities"""
    if request.method == 'GET':
        amenitiesList = []
        allAmenities = models.storage.all(classes["Amenity"])
        for val in allAmenities.values():
            amenitiesList.append(val.to_dict())
        return amenitiesList
    if request.method == 'POST':
        try:
            body = request.get_json()
        except Exception as e:
            abort(400, "Not a JSON")
        if body.get("name") is None:
            abort(400, "Missing name")
        newObj = Amenity(**body)
        models.storage.new(newObj)
        models.storage.save()
        return newObj.to_dict(), 201


@app_views.route('/amenities/<amenities_id>',
                 methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def amenity_http_methods(amenities_id):
    """methods for GET, PUT, and DELETE using id variable"""
    amenitiesNeeded = models.storage.get(classes["Amenity"], amenities_id)
    if request.method == 'GET':
        if amenitiesNeeded:
            return amenitiesNeeded.to_dict()
        abort(404)
    if request.method == 'DELETE':
        if amenitiesNeeded:
            models.storage.delete(amenitiesNeeded)
            models.storage.save()
            return {}
        abort(404)
    if request.method == 'PUT':
        try:
            body = request.get_json()
        except Exception as e:
            abort(400, "Not a JSON")
            amenObj = models.storage.get(classes["Amenity"], amenities_id)
            if not amenObj:
                abort(404)
            for key, val in body.items():
                if key not in ["id", "created_at", "updated_at"]:
                    setattr(amenObj, key, val)
            models.storage.save()
            return amenObj.to_dict()
