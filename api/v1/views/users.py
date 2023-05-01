#!/usr/bin/python3
"""Handle user objects"""
from ast import mod
import re
import hashlib
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
hash_object = hashlib.md5()

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def work_on_users():
    """working on users"""
    if request.method == 'GET':
        users = models.storage.all(classes['User'])
        user_list = []
        for v in users.values():
            user_list.append(v.to_dict())
        return jsonify(user_list)
    if request.method == 'POST':
        body = request.get_json()
        if not body:
            abort(400, "Not a JSON")
        if not body.get('email'):
            abort(400, "Missing email")
        if not body.get('password'):
            abort(400, "Missing password")
        hash_object.update(body["password"].encode())
        hex_digit = hash_object.hexdigest()
        new_user = User(**body)
        setattr(new_user, 'password', hex_digit)
        models.storage.new(new_user)
        models.storage.save()
        return make_response(jsonify(new_user.to_dict(), 201))


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def work_on_a_user(user_id):
    """working on users"""
    if request.method == 'GET':
        user = models.storage.get(classes['User'], user_id)
        if not user:
            abort(404)
        return jsonify(user.to_dict())
    if request.method == 'DELETE':
        user = models.storage.get(classes['User'], user_id)
        if not user:
            abort(404)
        models.storage.delete(user)
        models.storage.save()
        return jsonify({})
    if request.method == 'PUT':
        user = models.storage.get(classes['User'], user_id)
        if not user:
            abort(404)
        body = request.get_json()
        if not body:
            abort(400, "Not a JSON")
        for k, v in body.items():
            if k not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, k, v)
        models.storage.save()
        return jsonify(user.to_dict())
