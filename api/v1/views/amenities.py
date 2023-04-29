#!/usr/bin/python3
"""amenity view Module"""
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from api.v1.views import *
from flask import jsonify, request, abort


@app_views.route('/amenities', strict_slashes=False,
                 methods=['GET'])
def get_all_amenities():
    """function that retrieves all the amenitys in database"""
    all_amenities = storage.all(Amenity)
    amenity = []
    for items in all_amenities.values():
        amenity.append(items.to_dict())
    return jsonify(amenity)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET'])
def get_a_amenity(amenity_id):
    """function that retrieves a amenity in database"""
    an_amenity = storage.get(Amenity, amenity_id)
    if not an_amenity:
        abort(404)
    return jsonify(an_amenity.to_dict()), 200


@app_views.route('/amenities', strict_slashes=False,
                 methods=['POST'])
def create_an_amenity():
    """function that creates a amenity in database"""
    post_amenity = request.get_json()
    get_name = post_amenity.get('name')
    if type(post_amenity) != dict:
        return jsonify({"Error": "Not a JSON"}), 400
    if get_name is None:
        return jsonify({"Error": "Missing name"}), 400
    add_amenity = Amenity(**post_amenity)
    add_amenity.save()
    return jsonify(add_amenity.to_dict()), 201
    

@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_a_amenity(amenity_id):
    """function that deletes a amenity in database"""
    a_amenity = storage.get(Amenity, amenity_id)
    storage.delete(a_amenity)
    storage.save()
    if not a_amenity:
        abort(404)
    return jsonify({}), 200


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['PUT'])
def update_a_amenity(amenity_id):
    """function that updatess a amenity in database"""
    a_amenity = storage.get(Amenity, amenity_id)
    update_amenity = request.get_json()
    ignore_keys = ["id", "created_at", "updated_at"]

    if type(update_amenity) != dict:
        return jsonify({"Error": "Not a JSON"}), 400
    for keys, values in update_amenity.items():
        if keys not in ignore_keys:
            setattr(a_amenity, keys, values)
            storage.save()
    return jsonify(a_amenity.to_dict()), 200
