#!/usr/bin/python3
"""Setup view blueprints"""
from flask import Blueprint
from api.v1.views.index import *

app_views = Blueprint('app_views_blueprint', __name__)

