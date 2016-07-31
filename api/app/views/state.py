from flask import jsonify, request
from flask_json import json_response
from app.models.state import State
from app import app
from peewee import *

@app.route('/states', methods=['GET','POST'])
def states():
    ''' states returns a list of all states in the database in the case of a GET request, and creates a new state in the database in the case of a POST request '''
    if request.method == 'GET':
        list = []
        for record in State.select():
            hash = record.to_hash()
            list.append(hash)
        return jsonify(list)

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

@app.route('/states/<state_id>', methods=['GET','DELETE'])
def state_id(state_id):
    ''' '''
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
    if request.method == 'GET':
        return jsonify(record.to_hash())

    elif request.method == "DELETE":
        record.delete_instance()
        record.save()
        return 'deleted state\n'
