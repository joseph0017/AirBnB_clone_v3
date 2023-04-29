#!/usr/bin/python3
"""cities view Module"""
from models.review import Review
from models import storage
from api.v1.views import app_views
from api.v1.views import *
from flask import jsonify, request, abort


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['GET'])
def get_all_reviews(place_id):
    """function that retrieves all the reviews in database"""
    place = storage.get(Review, place_id)
    review = []
    if not place:
        return jsonify({"error": "Not found"})
    for items in place.reviews:
        review.append(items.to_dict())
    return jsonify(review)


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['GET'])
def get_a_review(review_id):
    """function that retrieves a review in database"""
    a_review = storage.get(Review, review_id)
    if not a_review:
        abort(404)
    return jsonify(a_review.to_dict()), 200


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['POST'])
def create_a_review(place_id):
    """function that creates a review in database"""
    post_review = request.get_json()
    get_text = post_review.get('text')
    get_place_id = post_review.get('user_id')
    if type(post_review) != dict:
        return jsonify({"Error": "Not a JSON"}), 400
    if get_text is None:
        return jsonify({"Error": "Missing text"}), 400
    if get_place_id is None:
        return jsonify({"Error": "Missing user_id"}), 400
    if not storage.get('User', get_place_id):
        abort(404)
    add_review = Review(place_id=place_id, **post_review)
    add_review.save()
    return jsonify(add_review.to_dict()), 201
    

@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_a_review(review_id):
    """function that deletes a review in database"""
    a_review = storage.get(Review, review_id)
    storage.delete(a_review)
    storage.save()
    if not a_review:
        abort(404)
    return jsonify({}), 200


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['PUT'])
def update_a_review(review_id):
    """function that updatess a review in database"""
    a_review = storage.get(Review, review_id)
    update_review = request.get_json()
    ignore_keys = ["id", "created_at", "updated_at", "place_id", "user_id"]

    if type(update_review) != dict:
        return jsonify({"Error": "Not a JSON"}), 400
    for keys, values in update_review.items():
        if keys not in ignore_keys:
            setattr(a_review, keys, values)
            storage.save()
    return jsonify(a_review.to_dict()), 200
