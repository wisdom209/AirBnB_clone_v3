#!/usr/bin/python3
"""Setup view blueprints"""
from flask import Blueprint, jsonify
app_views = Blueprint('app_views_blueprint', __name__, url_prefix='/api/v1')
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.index import *
from api.v1.views.amenities import *
from api.v1.views.places import *
