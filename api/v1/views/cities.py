#!/usr/bin/python3
"""starts a cities route"""
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET', 'POST'])
def city_by_state(state_id):
    """performs CRUD on city objects"""
    if request.method == 'GET':
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        cities = [city.to_dict() for city in state.cities]
        return jsonify(cities)

    if request.method == 'POST':
        params = request.get_json(silent=True)
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        if not params:
            return make_response("Not a JSON\n", 400)
        if 'name' not in params:
            return make_response("Missing name\n", 400)
        params['state_id'] = state_id
        new = City(**params)
        new.save()
        return jsonify(new.to_dict()), 201


@app_views.route("/cities/<city_id>", strict_slashes=False,
                 methods=['GET', 'PUT', 'DELETE'])
def cities(city_id):
    if request.method == 'GET':
        if city_id is None:
            abort(404)
        else:
            city = storage.get(City, city_id)
            if city is None:
                abort(404)
            return jsonify(city.to_dict())

    if request.method == 'DELETE':
        city = storage.get(City, city_id)
        if city is not None:
            storage.delete(city)
            storage.save()
            return jsonify({})
        abort(404)

    if request.method == 'PUT':
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        params = request.get_json(silent=True)
        if not params:
            return make_response("Not a JSON\n", 400)
        for k in ("id", "state_id", "created_at", "updated_at"):
            params.pop(k, None)
        for k, v in params.items():
            setattr(city, k, v)
        city.save()
        return jsonify(city.to_dict())
