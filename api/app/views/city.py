from flask import jsonify, request
from flask_json import json_response
from peewee import *

from app.models.city import City
from app import app


@app.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def city(state_id):
    """Handle GET and POST requests to /states/<state_id>/cities route.

    Return a list of all cities in state (according to database) in the case of
    a GET request.
    Create a new city record in the given state in the database in the case of
    a POST request.
    """
    # handle GET requests:
    # --------------------------------------------------------------------------
    if request.method == 'GET':
        list = []
        for record in City.select().where(City.state == state_id):
            hash = record.to_hash()
            list.append(hash)
        return jsonify(list)

    # handle POST requests:
    # --------------------------------------------------------------------------
    elif request.method == 'POST':
        try:
            record = City(name=request.form["name"], state=state_id)
            record.save()
            return jsonify(record.to_hash())

        # return 409 if city with given name already exists
        except IntegrityError:
                return json_response(
                    add_status_=False,
                    status_=409,
                    code=10002,
                    msg="City already exists in this state"
                )


@app.route('/states/<state_id>/cities/<city_id>', methods=['GET', 'DELETE'])
def city_id(state_id, city_id):
    """Handle GET and DELETE requests to /states/<state_id>/cities/<city_id>.

    Return a hash of the appropriate record in the case of a GET request.
    Delete appropriate record in case of DELETE request.
    """
    # check whether resource exists:
    # --------------------------------------------------------------------------
    try:
        record = City.get(City.id == city_id)

    # return 404 not found if it does not
    except City.DoesNotExist:
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
        record.delete_instance()
        record.save()
        return 'deleted city\n'
