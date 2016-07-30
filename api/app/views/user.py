from flask import jsonify, request
from flask_json import json_response
from app.models.user import User
from app import app
from peewee import *

@app.route('/users', methods=['GET','POST'])
def users():
    ''' users returns a list of all users in the database in the case of a GET request, and creates a new user in the database in the case of a POST request '''
    if request.method == 'GET':
        list = []
        for record in User.select():
            hash = record.to_hash()
            list.append(hash)
        return jsonify(list)

    elif request.method == 'POST':
        usr_email = request.form["email"]
        usr_password = request.form["password"]
        usr_first_name = request.form["first_name"]
        usr_last_name = request.form["last_name"]

        try:
            record = User(email=usr_email, password=usr_password, first_name=usr_first_name, last_name=usr_last_name)
            record.save()
            return jsonify(record.to_hash())
        except:
            return json_response(add_status_=False, status_=409, code=10000, msg="Email already exists")

@app.route('/users/<user_id>', methods=['GET','PUT', 'DELETE'])
def user_id(user_id):
    ''' '''
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
    if request.method == 'GET':
        return jsonify(record.to_hash())

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

    elif request.method == "DELETE":
        record.delete_instance()
        record.save()
        return 'deleted user\n'
