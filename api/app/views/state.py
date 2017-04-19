from flask import jsonify, request
from flask_json import json_response
from peewee import *

from app.views.return_styles import ListStyle
from app.models.state import State
from app import app


@app.route('/states', methods=['GET', 'POST'])
def states():
    """Handle GET and POST requests to /states route.

     Return a list of all states in the database in the case of a GET request.
     Create a new state in the database in the case of a POST request
    """
    # handle GET requests:
    # --------------------------------------------------------------------------
    if request.method == 'GET':
        list = ListStyle.list(State.select(), request)
        return jsonify(list)

    # handle POST requests:
    # --------------------------------------------------------------------------
    elif request.method == 'POST':
        try:
            record = State(name=request.form["name"])
            record.save()
            return jsonify(record.to_hash())

        # return 409 state with given name already exists
        except IntegrityError:
                return json_response(
                    add_status_=False,
                    status_=409,
                    code=10001,
                    msg="State already exists"
                )


@app.route('/states/<state_id>', methods=['GET', 'DELETE'])
def state_id(state_id):
    """Handle GET and DELETE requests to /states/<state_id> route.

     Return a hash of the appropriate record in the database in the case of a
     GET request.
     Delete the appropriate record in the case of a DELETE request.
     """
    # check whether resource exists:
    # --------------------------------------------------------------------------
    try:
        record = State.get(State.id == state_id)

    # return 404 not found if it does not
    except State.DoesNotExist:
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
        return 'deleted state\n'
