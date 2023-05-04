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
# @app_views.route('/status', strict_slashes=False)
# def get_status():
#     """return the status"""
#     return jsonify({"status": "Ok"})


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def get_all_states():
    """retrieve the states"""
    if request.method == 'GET':
        state_list = []
        all_states = models.storage.all(classes["State"])
        for value in all_states.values():
            state_list.append(value.to_dict())
        return state_list
    if request.method == 'POST':
        try:
            body = request.get_json()
            if not body:
                abort(400, "Not a JSON")
            if body.get('name') is None:
                abort(400, 'Missing name')
            new_obj = State(**body)
            models.storage.new(new_obj)
            models.storage.save()
            return make_response(new_obj.to_dict(), 201)
        except Exception as e:
            abort(400)


@app_views.route('/states/<state_id>',
                 methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def work_on_a_state(state_id):
    """retrieve a states"""
    if request.method == 'GET':
        state_needed = models.storage.get(classes["State"], state_id)
        if state_needed:
            return (state_needed.to_dict())
        abort(404)
    if request.method == 'DELETE':
        state_needed = models.storage.get(classes["State"], state_id)
        if state_needed:
            models.storage.delete(state_needed)
            models.storage.save()
            return {}
        abort(404)
    if request.method == 'PUT':
        try:
            body = request.get_json()
            if not body:
                return abort(400, "Not a JSON")
            state_obj = models.storage.get(classes['State'], state_id)
            if not state_obj:
                abort(404)
            for k, v in body.items():
                if k not in ['id', 'created_at', 'updated_at']:
                    setattr(state_obj, k, v)
            models.storage.save()
            return state_obj.to_dict()
        except Exception as e:
            abort(404)


# 0e391e25-dd3a-45f4-bce3-4d1dea83f3c7
# 10098698-bace-4bfb-8c0a-6bae0f7f5b8f oregon
