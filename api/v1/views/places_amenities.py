#!/usr/bin/python3
"""starts a amenities route"""
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort
from models import storage, storage_t
from models.place import Place
from models.amenity import Amenity


@app_views.route('places/<place_id>/amenities', strict_slashes=False,
                 methods=['GET'])
def amenity_by_place(place_id):
    """performs CRUD on amenity objects"""
    if request.method == 'GET':
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        amenities = [amenity.to_dict() for amenity in place.amenities]
        return jsonify(amenities)


@app_views.route('places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False,
                 methods=['DELETE', 'POST'])
def amenity_delete_link(place_id, amenity_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if request.method == 'POST':
        if storage_t == 'db':
            if amenity not in place.amenities:
                place.amenities.append(amenity)
                place.save()
                return jsonify(amenity.to_dict()), 201
            return jsonify(amenity.to_dict())
        else:
            if amenity_id not in place.amenity_ids:
                place.amenity_ids.append(amenity_id)
                place.save()
                return jsonify(amenity.to_dict()), 201
            return jsonify(amenity.to_dict())

    if request.method == 'DELETE':
        if storage_t == 'db':
            if amenity not in place.amenities:
                abort(404)
            place.amenities.remove(amenity)
            place.save()
            return jsonify({})
        else:
            if amenity_id not in place.amenity_ids:
                abort(404)
            place.amenity_ids.remove(amenity_id)
            place.save()
            return jsonify({})
