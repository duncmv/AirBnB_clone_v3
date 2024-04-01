#!/usr/bin/python3
"""starts a reviews route"""
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('places/<place_id>/reviews', strict_slashes=False,
                 methods=['GET', 'POST'])
def review_by_place(place_id):
    """performs CRUD on review objects"""
    if request.method == 'GET':
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        reviews = [review.to_dict() for review in place.reviews]
        return jsonify(reviews)

    if request.method == 'POST':
        params = request.get_json(silent=True)
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        if not params:
            return make_response("Not a JSON\n", 400)
        if 'user_id' not in params:
            return make_response("Missing user_id\n", 400)
        user = storage.get(User, params['user_id'])
        if user is None:
            abort(404)
        if 'text' not in params:
            return make_response("Missing text\n", 400)
        params['place_id'] = place_id
        new = Review(**params)
        new.save()
        return jsonify(new.to_dict()), 201


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=['GET', 'PUT', 'DELETE'])
def reviews(review_id):
    if request.method == 'GET':
        if review_id is None:
            abort(404)
        else:
            review = storage.get(Review, review_id)
            if review is None:
                abort(404)
            return jsonify(review.to_dict())

    if request.method == 'DELETE':
        review = storage.get(Review, review_id)
        if review is not None:
            storage.delete(review)
            storage.save()
            return jsonify({})
        abort(404)

    if request.method == 'PUT':
        review = storage.get(Review, review_id)
        if review is None:
            abort(404)
        params = request.get_json(silent=True)
        if not params:
            return make_response("Not a JSON\n", 400)
        for k in ("id", "user_id", "place_id", "created_at", "updated_at"):
            params.pop(k, None)
        for k, v in params.items():
            setattr(review, k, v)
        review.save()
        return jsonify(review.to_dict())
