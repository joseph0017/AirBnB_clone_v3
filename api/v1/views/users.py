#!/usr/bin/python3
"""user view Module"""
from models.user import User
from models import storage
from api.v1.views import app_views
from api.v1.views import *
from flask import jsonify, request, abort


@app_views.route('/users', strict_slashes=False,
                 methods=['GET'])
def get_all_users():
    """function that retrieves all the users in database"""
    all_users = storage.all(User)
    user = []
    for items in all_users.values():
        user.append(items.to_dict())
    return jsonify(user)


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['GET'])
def get_a_user(user_id):
    """function that retrieves a user in database"""
    a_user = storage.get(User, user_id)
    if not a_user:
        abort(404)
    return jsonify(a_user.to_dict()), 200


@app_views.route('/users', strict_slashes=False,
                 methods=['POST'])
def create_a_user():
    """function that creates a user in database"""
    post_user = request.get_json()
    get_email = post_user.get('email')
    get_password = post_user.get('password')
    if type(post_user) != dict:
        return jsonify({"Error": "Not a JSON"}), 400
    if get_email is None:
        return jsonify({"Error": "Missing email"}), 400
    if get_password is None:
        return jsonify({"Error": "Missing password"}), 400
    add_user = User(**post_user)
    add_user.save()
    return jsonify(add_user.to_dict()), 201
    

@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_a_user(user_id):
    """function that deletes a user in database"""
    a_user = storage.get(User, user_id)
    storage.delete(a_user)
    storage.save()
    if not a_user:
        abort(404)
    return jsonify({}), 200


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['PUT'])
def update_a_user(user_id):
    """function that updatess a user in database"""
    a_user = storage.get(User, user_id)
    update_user = request.get_json()
    ignore_keys = ["id", "created_at", "updated_at"]

    if type(update_user) != dict:
        return jsonify({"Error": "Not a JSON"}), 400
    for keys, values in update_user.items():
        if keys not in ignore_keys:
            setattr(a_user, keys, values)
            storage.save()
    return jsonify(a_user.to_dict()), 200
