from flask import jsonify, request
from flask_json import json_response
from peewee import *

from app.models.review import Review
from app.models.review_user import ReviewUser
from app.models.review_place import ReviewPlace
from app.models.user import User
from app import app


@app.route('/users/<user_id>/reviews', methods=['GET', 'POST'])
def user_reviews(user_id):
    """Handle GET and POST requests to /users/<user_id>/reviews route.

    Return a list of all reviews for given user in the database in the case of
    a GET request.
    Create a new user review in the database in the case of a POST request.
    """
    # handle GET requests:
    # --------------------------------------------------------------------------
    if request.method == 'GET':
        list = []
        for record in ReviewUser.select().where(ReviewUser.user == user_id):
            hash = record.review.to_hash()
            list.append(hash)
        return jsonify(list)

    # handle POST requests:
    # --------------------------------------------------------------------------
    elif request.method == 'POST':
        record = Review(
            message=request.form["message"],
            user=request.form["user_id"],
            stars=request.form["stars"]
        )
        record.save()

        u_review = ReviewUser(
            user=user_id,
            review=record.id
        )
        u_review.save()

        return jsonify(record.to_hash())


@app.route('/users/<user_id>/reviews/<review_id>', methods=['GET', 'PUT', 'DELETE'])
def review_user_id(user_id, review_id):
    """Handle GET and DELETE requests to /users/<user_id>/reviews/<review_id>.

    Return a hash representing user review in the case of a GET request.
    Delete appropriate records for user review in case of DELETE request.
    """
    # check whether resource exists:
    # --------------------------------------------------------------------------
    try:
        record = Review.get(Review.id == review_id)

    # return 404 not found if it does not
    except Review.DoesNotExist:
        return json_response(
            add_status_=False,
            status_=404,
            code=404,
            msg="not found"
        )

    # if exception does not arise:
    # --------------------------------------------------------------------------
    # handle GET requests
    if request.method == 'GET':
        return jsonify(record.to_hash())

    # handle DELETE requests
    elif request.method == "DELETE":
        ur_record = ReviewUser.select().where(ReviewUser.review == review_id)
        ur_record.delete_instance()
        ur_record.save()
        record.delete_instance()
        record.save()
        return 'deleted review record\ndeleted review user record\n'


@app.route('/places/<place_id>/reviews', methods=['GET', 'POST'])
def place_reviews(place_id):
    """Handle GET and POST requests to /places/<place_id>/reviews route.

    Return a list of all reviews for given place in the database in the case of
    a GET request.
    Create a new place review in the database in the case of a POST request.
    """
    # handle GET requests:
    # --------------------------------------------------------------------------
    if request.method == 'GET':
        list = []
        for record in ReviewPlace.select().where(ReviewPlace.place == place_id):
            hash = record.review.to_hash()
            list.append(hash)
        return jsonify(list)

    # handle POST requests:
    # --------------------------------------------------------------------------
    elif request.method == 'POST':
        record = ReviewPlace(
            message=request.form["message"],
            user=request.form["user_id"],
            stars=request.form["stars"]
        )
        record.save()

        p_review = ReviewUser(
            place=place_id,
            review=record.id
        )
        p_review.save()

        return jsonify(record.to_hash())


@app.route('/places/<place_id>/reviews/<review_id>', methods=['GET', 'PUT', 'DELETE'])
def review_place_id(place_id, review_id):
    """Handle GET and DELETE requests to /places/<place_id>/reviews/<review_id>.

    Return a hash representing place review in the case of a GET request.
    Delete appropriate records for place review in case of DELETE request.
    """
    # check whether resource exists:
    # --------------------------------------------------------------------------
    try:
        record = Review.get(Review.id == review_id)

    # return 404 not found if it does not
    except Review.DoesNotExist:
        return json_response(
            add_status_=False,
            status_=404,
            code=404,
            msg="not found"
        )

    # if exception does not arise:
    # --------------------------------------------------------------------------
    # handle GET requests
    if request.method == 'GET':
        return jsonify(record.to_hash())

    # handle DELETE requests
    elif request.method == "DELETE":
        pr_record = ReviewPlace.select().where(ReviewPlace.review == review_id)
        pr_record.delete_instance()
        pr_record.save()
        record.delete_instance()
        record.save()
        return 'deleted review record\ndeleted review place record\n'
