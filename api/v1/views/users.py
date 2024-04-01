#!/usr/bin/python3
"""starts a users route"""
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort
from models import storage
from models.user import User


@app_views.route("/users", strict_slashes=False,
                 methods=['GET', 'POST'])
@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def user(user_id=None):
    """performs CRUD on user objects"""
    if request.method == 'GET':
        if user_id is None:
            all = [user.to_dict() for user in storage.all(User).values()]
            return jsonify(all)
        else:
            user = storage.get(User, user_id)
            if user is None:
                abort(404)
            return jsonify(user.to_dict())

    if request.method == 'DELETE':
        user = storage.get(User, user_id)
        if user is not None:
            storage.delete(user)
            storage.save()
            return jsonify({})
        abort(404)

    if request.method == 'POST':
        params = request.get_json(silent=True)
        if not params:
            return make_response("Not a JSON\n", 400)
        if 'email' not in params:
            return make_response("Missing email\n", 400)
        if 'password' not in params:
            return make_response("Missing password\n", 400)
        new = User(**params)
        new.save()
        return jsonify(new.to_dict()), 201

    if request.method == 'PUT':
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        params = request.get_json(silent=True)
        if not params:
            return make_response("Not a JSON\n", 400)
        for k in ("id", "email", "created_at", "updated_at"):
            params.pop(k, None)
        for k, v in params.items():
            setattr(user, k, v)
        user.save()
        return jsonify(user.to_dict())
