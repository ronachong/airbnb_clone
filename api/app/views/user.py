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
    if request.method == 'GET':
        record = User.get(User.id == user_id)
        return jsonify(record.to_hash())

    elif request.method == 'PUT':
        key = request.values.keys()[0]
        record = User.get(User.id == user_id)
        if key == "last_name":
            record.last_name = request.values[key]
        if key == "first_name":
            record.first_name = request.values[key]
        if key == "password":
            record.password = request.values[key]
        if key == "is_admin":
            record.is_admin = request.values[key]
        record.save()
        return jsonify(record.to_hash())

    elif request.method == "DELETE":
        record = User.get(User.id == user_id)
        record.delete_instance()
        record.save()
        return 'deleted user\n'
