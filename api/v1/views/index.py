#!/usr/bin/python3
"""starts a route"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """returns the status"""
    return jsonify(status="OK")
