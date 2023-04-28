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
