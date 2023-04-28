#!/usr/bin/python3
"""cities view Module"""
from models.city import City
from models import storage
from api.v1.views import app_views
from api.v1.views import *
from flask import jsonify, request, abort


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET'])
def get_all_cities(state_id):
    """function that retrieves all the citys in database"""
    state = storage.get(State, state_id)
    city = []
    if not state:
        return jsonify({"error": "Not found"})
    for items in state.cities:
        city.append(items.to_dict())
    return jsonify(city)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['GET'])
def get_a_city(city_id):
    """function that retrieves a city in database"""
    a_city = storage.get(City, city_id)
    if not a_city:
        abort(404)
    return jsonify(a_city.to_dict()), 200


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def create_a_city(state_id):
    """function that creates a city in database"""
    post_city = request.get_json()
    get_name = post_city.get('name')
    if type(post_city) != dict:
        return jsonify({"Error": "Not a JSON"}), 400
    if get_name is None:
        return jsonify({"Error": "Missing name"}), 400
    add_city = City(state_id=state_id, **post_city)
    add_city.save()
    return jsonify(add_city.to_dict()), 201
    

@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_a_city(city_id):
    """function that deletes a city in database"""
    a_city = storage.get(City, city_id)
    storage.delete(a_city)
    storage.save()
    if not a_city:
        abort(404)
    return jsonify({}), 200


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['PUT'])
def update_a_city(city_id):
    """function that updatess a city in database"""
    a_city = storage.get(City, city_id)
    update_city = request.get_json()
    ignore_keys = ["id", "created_at", "updated_at"]

    if type(update_city) != dict:
        return jsonify({"Error": "Not a JSON"}), 400
    for keys, values in update_city.items():
        if keys not in ignore_keys:
            setattr(a_city, keys, values)
            storage.save()
    return jsonify(a_city.to_dict()), 200
