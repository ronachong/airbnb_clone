from flask import jsonify, request
from flask_json import json_response
from peewee import *

from app.views.return_styles import ListStyle
from app.models.user import User
from app import app


@app.route('/users', methods=['GET', 'POST'])
def users():
    """Handle GET and POST requests to /users route.

    Return a list of all users in the database in the case of a GET request.
    Create a new user record in the database in the case of a POST request.
    """
    # handle GET requests:
    # --------------------------------------------------------------------------
    if request.method == 'GET':
        list = ListStyle.list(User.select(), request)
        return jsonify(list)

    # handle POST requests:
    # --------------------------------------------------------------------------
    elif request.method == 'POST':
        try:
            record = User(
                email=request.form["email"],
                password=request.form["password"],
                first_name=request.form["first_name"],
                last_name=request.form["last_name"]
            )
            record.save()
            return jsonify(record.to_hash())

        # return 409 if user with given email already exists
        except IntegrityError:
            return json_response(
                add_status_=False,
                status_=409,
                code=10000,
                msg="Email already exists"
            )


@app.route('/users/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def user_id(user_id):
    """Handle GET, PUT and DELETE requests to /users/<user_id> route.

    Return a hash of the appropriate record in the case of a GET request.
    Update appropriate hash in database in case of PUT request.
    Delete appropriate record in case of DELETE request.
    """
    # check whether resource exists:
    # --------------------------------------------------------------------------
    try:
        record = User.get(User.id == user_id)

    # return 404 not found if it does not
    except User.DoesNotExist:
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

    # handle PUT requests
    elif request.method == 'PUT':
        # code below can be optimized in future using list comprehensions
        for key in request.values.keys():
            if key == "last_name":
                record.last_name = request.values[key]
            elif key == "first_name":
                record.first_name = request.values[key]
            elif key == "password":
                record.password = request.values[key]
            elif key == "is_admin":
                record.is_admin = request.values[key]
            elif key == "email":
                record.email = request.values[key]
        record.save()
        return jsonify(record.to_hash())

    # handle DELETE requests
    elif request.method == "DELETE":
        record.delete_instance()
        record.save()
        return 'deleted user\n'
