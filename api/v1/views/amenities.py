#!/usr/bin/python3
"""starts a amenities route"""
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", strict_slashes=False,
                 methods=['GET', 'POST'])
@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def amenity(amenity_id=None):
    """performs CRUD on amenity objects"""
    if request.method == 'GET':
        if amenity_id is None:
            all = [am.to_dict() for am in storage.all(Amenity).values()]
            return jsonify(all)
        else:
            amenity = storage.get(Amenity, amenity_id)
            if amenity is None:
                abort(404)
            return jsonify(amenity.to_dict())

    if request.method == 'DELETE':
        amenity = storage.get(Amenity, amenity_id)
        if amenity is not None:
            storage.delete(amenity)
            storage.save()
            return jsonify({})
        abort(404)

    if request.method == 'POST':
        params = request.get_json(silent=True)
        if not params:
            return make_response("Not a JSON\n", 400)
        if 'name' not in params:
            return make_response("Missing name\n", 400)
        new = Amenity(**params)
        new.save()
        return jsonify(new.to_dict()), 201

    if request.method == 'PUT':
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)
        params = request.get_json(silent=True)
        if not params:
            return make_response("Not a JSON\n", 400)
        for k in ("id", "created_at", "updated_at"):
            params.pop(k, None)
        for k, v in params.items():
            setattr(amenity, k, v)
        amenity.save()
        return jsonify(amenity.to_dict())
