#!/usr/bin/python3
"""State view Module"""
from models.state import State
from models import storage
from api.v1.views import app_views
from api.v1.views import *
from flask import jsonify, request, abort


@app_views.route('/states', strict_slashes=False,
                 methods=['GET'])
def get_all_states():
    """function that retrieves all the states in database"""
    all_states = storage.all(State)
    state = []
    for items in all_states.values():
        state.append(items.to_dict())
    return jsonify(state)


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['GET'])
def get_a_state(state_id):
    """function that retrieves a state in database"""
    a_state = storage.get(State, state_id)
    if not a_state:
        abort(404)
    return jsonify(a_state.to_dict()), 200


@app_views.route('/states', strict_slashes=False,
                 methods=['POST'])
def create_a_state():
    """function that creates a state in database"""
    post_state = request.get_json()
    get_name = post_state.get('name')
    if type(post_state) != dict:
        return jsonify({"Error": "Not a JSON"}), 400
    if get_name is None:
        return jsonify({"Error": "Missing name"}), 400
    add_state = State(**post_state)
    add_state.save()
    return jsonify(add_state.to_dict()), 201
    

@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_a_state(state_id):
    """function that deletes a state in database"""
    a_state = storage.get(State, state_id)
    storage.delete(a_state)
    storage.save()
    if not a_state:
        abort(404)
    return jsonify({}), 200


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['PUT'])
def update_a_state(state_id):
    """function that updatess a state in database"""
    a_state = storage.get(State, state_id)
    update_state = request.get_json()
    ignore_keys = ["id", "created_at", "updated_at"]

    if type(update_state) != dict:
        return jsonify({"Error": "Not a JSON"}), 400
    for keys, values in update_state.items():
        if keys not in ignore_keys:
            setattr(a_state, keys, values)
            storage.save()
    return jsonify(a_state.to_dict()), 200
