#!/usr/bin/python3
"""Setup view blueprints"""
from api.v1.views.states import *
from api.v1.views.index import *
from flask import Blueprint, jsonify
app_views = Blueprint('app_views_blueprint', __name__, url_prefix='/api/v1')
