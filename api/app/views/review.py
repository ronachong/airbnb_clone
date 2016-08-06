from flask import jsonify, request
from flask_json import json_response
from peewee import *

from app.models.review import Review
from app.models.review_user import ReviewUser
from app.models.user import User
from app import app


@app.route('/users/<user_id>/reviews', methods=['GET', 'POST'])
def reviews():
    """Handle GET and POST requests to /users route.

    Return a list of all reviews for given user in the database in the case of
    a GET request.
    Create a new user review in the database in the case of a POST request.
    """
    # handle GET requests:
    # --------------------------------------------------------------------------
    if request.method == 'GET':
        list = []
        for record in ReviewUser.select().where(ReviewUser.user.id == user_id):
            hash = record.review.to_hash()
            list.append(hash)
        return jsonify(list)

    # handle POST requests:
    # --------------------------------------------------------------------------
    elif request.method == 'POST':
        record = ReviewUser(
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
