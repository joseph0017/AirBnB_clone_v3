#!/usr/bin/python3
"""cities view Module"""
from models.place import Place
from models import storage
from api.v1.views import app_views
from api.v1.views import *
from flask import jsonify, request, abort


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['GET'])
def get_all_places(city_id):
    """function that retrieves all the places in database"""
    state = storage.get(Place, city_id)
    place = []
    if not state:
        return jsonify({"error": "Not found"})
    for items in state.cities:
        place.append(items.to_dict())
    return jsonify(place)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['GET'])
def get_a_place(place_id):
    """function that retrieves a place in database"""
    a_place = storage.get(Place, place_id)
    if not a_place:
        abort(404)
    return jsonify(a_place.to_dict()), 200


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['POST'])
def create_a_place(city_id):
    """function that creates a place in database"""
    post_place = request.get_json()
    get_name = post_place.get('name')
    get_user_id = post_place.get('user_id')
    if type(post_place) != dict:
        return jsonify({"Error": "Not a JSON"}), 400
    if get_name is None:
        return jsonify({"Error": "Missing name"}), 400
    if get_user_id is None:
        return jsonify({"Error": "Missing user_id"}), 400
    if not storage.get('User', get_user_id):
        abort(404)
    add_place = Place(city_id=city_id, **post_place)
    add_place.save()
    return jsonify(add_place.to_dict()), 201
    

@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_a_place(place_id):
    """function that deletes a place in database"""
    a_place = storage.get(Place, place_id)
    storage.delete(a_place)
    storage.save()
    if not a_place:
        abort(404)
    return jsonify({}), 200


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['PUT'])
def update_a_place(place_id):
    """function that updatess a place in database"""
    a_place = storage.get(Place, place_id)
    update_place = request.get_json()
    ignore_keys = ["id", "created_at", "updated_at"]

    if type(update_place) != dict:
        return jsonify({"Error": "Not a JSON"}), 400
    for keys, values in update_place.items():
        if keys not in ignore_keys:
            setattr(a_place, keys, values)
            storage.save()
    return jsonify(a_place.to_dict()), 200
