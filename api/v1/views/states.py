#!/usr/bin/python3
"""starts a states route"""
from api.v1.views import app_views
from flask import jsonify, request, make_response
from models import storage
from models.state import State

@app_views.route("/states", strict_slashes= False,
                 methods=['GET'])
@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['GET', 'POST', 'DELETE', 'PUT'])
def state(state_id=None):
    """performs CRUD on state objects"""
    if request.method == 'GET':
        if state_id is None:
            all = [state.to_dict() for state in storage.all(State).values()]
            return jsonify(all)
        else:
            state = storage.get(State, state_id)
            if state is None:
                return make_response(404)
            return jsonify(state.to_dict())
    
    if request.method == 'DELETE':
        state = storage.get(State, state_id)
        if state is not None:
            storage.delete(state)
            return 