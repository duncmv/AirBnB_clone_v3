#!/usr/bin/python3
"""starts a places route"""
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort
from models import storage, storage_t
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['GET', 'POST'])
def place_by_city(city_id):
    """performs CRUD on place objects"""
    if request.method == 'GET':
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        places = [place.to_dict() for place in city.places]
        return jsonify(places)

    if request.method == 'POST':
        params = request.get_json(silent=True)
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        if not params:
            return make_response("Not a JSON\n", 400)
        if 'user_id' not in params:
            return make_response("Missing user_id\n", 400)
        user = storage.get(User, params['user_id'])
        if user is None:
            abort(404)
        if 'name' not in params:
            return make_response("Missing name\n", 400)
        params['city_id'] = city_id
        new = Place(**params)
        new.save()
        return jsonify(new.to_dict()), 201


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=['GET', 'PUT', 'DELETE'])
def places(place_id):
    if request.method == 'GET':
        if place_id is None:
            abort(404)
        else:
            place = storage.get(Place, place_id)
            if place is None:
                abort(404)
            return jsonify(place.to_dict())

    if request.method == 'DELETE':
        place = storage.get(Place, place_id)
        if place is not None:
            storage.delete(place)
            storage.save()
            return jsonify({})
        abort(404)

    if request.method == 'PUT':
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        params = request.get_json(silent=True)
        if not params:
            return make_response("Not a JSON\n", 400)
        for k in ("id", "user_id", "city_id", "created_at", "updated_at"):
            params.pop(k, None)
        for k, v in params.items():
            setattr(place, k, v)
        place.save()
        return jsonify(place.to_dict())


@app_views.route("/places_search", strict_slashes=False,
                 methods=['POST'])
def place_search():
    """returns places based on json criteria"""
    params = request.get_json(silent=True)
    if params is None:
        return make_response("Not a JSON\n", 400)
    state_ids = params.get("states", [])
    city_ids = params.get("cities", [])
    amenity_ids = params.get("amenities", [])

    length_ids = len(state_ids) + len(city_ids) + len(amenity_ids)
    all_places = list(storage.all(Place).values())
    if length_ids == 0:
        return jsonify([p.to_dict() for p in all_places])

    pList = []
    state_cities = []

    if len(state_ids) != 0:
        for state_id in state_ids:
            state = storage.get("State", state_id)
            s_cities = state.cities
            state_cities.extend(list(s_cities))
        for city in state_cities:
            list_1 = [p for p in all_places if p.city_id == city.id]
            pList.extend(list_1)

    if len(city_ids) != 0:
        for city_id in city_ids:
            city = storage.get("City", city_id)
            if city not in state_cities:
                list_2 = [p for p in all_places if p.city_id == city_id]
                pList.extend(list_2)

    if len(amenity_ids) != 0:
        if len(state_ids) == 0 and len(city_ids) == 0:
            pList.extend(all_places)
        for amenity_id in amenity_ids:
            amenity = storage.get("Amenity", amenity_id)
            if storage_t == 'db':
                pList = [p for p in pList if amenity in p.amenities]
            else:
                pList = [p for p in pList if amenity_id in p.amenity_ids]

    return jsonify([p.to_dict() for p in pList])
