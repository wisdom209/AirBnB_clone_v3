#!/usr/bin/python3
"""Handle amenities objects"""
from ast import mod
import os
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
from api.v1.views import amenities, app_views

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


@app_views.route('/places/<place_id>/amenities', methods=['GET'], strict_slashes=False)
def work_on_amenities(place_id):
    """Perform http operations on amenities"""
    if request.method == 'GET':
        place = models.storage.get(Place, place_id)
        if not place:
            abort(404)
    amenities_dict_list = []
    if models.storage_t == 'db':
        amenities_list = place.amenities
        for val in amenities_list:
            amenities_dict_list.append(val.to_dict())
        return jsonify(amenities_dict_list)
    else:
        amenities_list = [models.storage.get(
            Amenity, _id) for _id in place.amenity_ids]
        return jsonify(amenities_list)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE', 'POST'], strict_slashes=False)
def work_on_amenities_specifically(place_id, amenity_id):
    """Perform http operations on amenities"""
    if request.method == 'DELETE':
        place = models.storage.get(Place, place_id)
        if not place:
            abort(404)
        amenity_obj = models.storage.get(Amenity, amenity_id)
        if not amenity_obj:
            abort(404)
        if models.storage_t == 'db':
            amenities_list = place.amenities
            for val in amenities_list:
                if val.id == amenity_id:
                    place.remove(val)
                    models.storage.save()
            return jsonify({})
        else:
            for _id in place.amenity_ids:
                if _id == amenity_id:
                    place.amenity_ids.remove(_id)
            models.storage.save()
            return jsonify({})
    if request.method == 'POST':
        place = models.storage.get(Place, place_id)
        if not place:
            abort(404)
        amenity_obj = models.storage.get(Amenity, amenity_id)
        if not amenity_obj:
            abort(404)
        if models.storage_t == 'db':
            if amenity_obj in place.amenities:
                return jsonify(amenity_obj.to_dict())
            place.amenities.append(amenity_obj)
            models.storage.save()
            return make_response(jsonify(amenity_obj.to_dict(), 201))
        else:
            for _id in place.amenity_ids:
                if _id == amenity_id:
                    return make_response(jsonify(amenity_obj.to_dict(), 200))
            place.amenity_ids.append(amenity_id)
            models.storage.save()
            return make_response(jsonify(amenity_obj.to_dict(), 201))
