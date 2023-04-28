#!/usr/bin/python3
"""Handle state objects"""
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


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'], strict_slashes=False)
def get_all_cities_by_stateId(state_id):
    """retrieve the state's cities"""
    if request.method == 'GET':
        city_list = []
        all_cities = models.storage.all(classes["City"])
        if not all_cities:
            abort(404)
        for value in all_cities.values():
            if value.state_id == state_id:
                city_list.append(value.to_dict())
        return city_list
    if request.method == 'POST':
        body = request.get_json()
        if not body:
            abort(404, "Not a JSON")
        


@ app_views.route('/cities/<city_id>', methods=['GET', 'DELETE'], strict_slashes=False)
def get_a_city(city_id):
    """get a city by id"""
    if request.method == 'GET':
        city = models.storage.get(classes["City"], city_id)
        if not city:
            abort(404)
        return city.to_dict()
    if request.method == 'DELETE':
        city = models.storage.get(classes["city"], city_id)
        if not city:
            abort(404)
        models.storage.delete(city)
        models.storage.save()
        return {}
