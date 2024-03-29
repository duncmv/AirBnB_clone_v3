#!/usr/bin/python3
"""starts a states route"""
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort
from models import storage
from models.state import State

@app_views.route("/states", strict_slashes= False,
                 methods=['GET', 'POST'])
@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def state(state_id=None):
    """performs CRUD on state objects"""
    if request.method == 'GET':
        if state_id is None:
            all = [state.to_dict() for state in storage.all(State).values()]
            return jsonify(all)
        else:
            state = storage.get(State, state_id)
            if state is None:
                abort(404)
            return jsonify(state.to_dict())

    if request.method == 'DELETE':
        state = storage.get(State, state_id)
        if state is not None:
            storage.delete(state)
            return jsonify({})
        abort(404)

    if request.method == 'POST':
        if not request.json:
            return "Not a JSON", 400
        if 'name' in request.json:
            return "Missing name", 400
        params = request.json
        new = State(**params)
        new.save()
        return jsonify(new.to_dict())
