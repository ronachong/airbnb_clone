from flask import jsonify, request
from flask_json import json_response
from peewee import *

from app.models.place import Place
from app import app


@app.route('/places', methods=['GET', 'POST'])
def places():
    """Handle GET and POST requests to /places route.

    Return a list of all places in the database in the case of a GET request.
    Create a new place record in the database in the case of a POST request.
    """
    # handle GET requests:
    # --------------------------------------------------------------------------
    if request.method == 'GET':
        list = []
        for record in Place.select():
            hash = record.to_hash()
            list.append(hash)
        return jsonify(list)

    # handle POST requests:
    # --------------------------------------------------------------------------
    elif request.method == 'POST':
        record = Place( owner=request.form['owner_id'],
                        city=request.form['city_id'],
                        name=request.form['name'],
                        description=request.form['description'],
                        number_rooms=request.form['number_rooms'],
                        number_bathrooms=request.form['number_bathrooms'],
                        max_guest=request.form['max_guest'],
                        price_by_night=request.form['price_by_night'],
                        latitude=request.form['latitude'],
                        longitude=request.form['longitude'] )
        record.save()
        return jsonify(record.to_hash())


@app.route('/places/<place_id>', methods=['GET', 'PUT', 'DELETE'])
def place_id(place_id):
    """Handle GET, PUT, and DELETE requests to /places/<place_id> route.

    Return a hash of the appropriate record in the case of a GET request.
    Update appropriate hash in database in case of PUT request.
    Delete appropriate record in case of DELETE request.
    """
    # check whether resource exists:
    # --------------------------------------------------------------------------
    try:
        record = Place.get(Place.id == place_id)

    # return 404 not found if it does not
    except Place.DoesNotExist:
        return json_response(
            add_status_=False,
            status_=404,
            code=404,
            msg="not found"
        )

    # if exception does not arise:
    if request.method == 'GET':
        return jsonify(record.to_hash())

    # if exception does not arise:
    # --------------------------------------------------------------------------
    # handle GET requests
    elif request.method == 'PUT':
        record = Place.get(Place.id == place_id)
        # code below can be optimized in future using list comprehensions
        for key in request.values.keys():
            if key == "name":
                record.name = request.values[key]
            elif key == "description":
                record.description = request.values[key]
            elif key == "number_rooms":
                record.number_rooms = request.values[key]
            elif key == "number_bathrooms":
                record.number_bathrooms = request.values[key]
            elif key == "max_guest":
                record.max_guest = request.values[key]
            elif key == "price_by_night":
                record.price_by_night = request.values[key]
            elif key == "latitude":
                record.latitude = request.values[key]
            elif key == "longitude":
                record.longitude = request.values[key]
            record.save()
        return jsonify(record.to_hash())

    # handle DELETE requests
    elif request.method == "DELETE":
        record.delete_instance()
        record.save()
        return 'deleted city\n'


@app.route('/states/<state_id>/cities/<city_id>/places', methods=['GET', 'POST'])
def city_places(state_id, city_id):
    """Handle GET & POST requests to /states/<state_id>/cities/<city_id>/places.

    Return a list of all places in the database in given city in the case of a
    GET request.
    Create a new place record in the given city in the database in the case of
    a POST request.
    """
    # handle GET requests:
    # --------------------------------------------------------------------------
    if request.method == 'GET':
        try:
            list = []
            for record in Place.select().where(Place.city == city_id):
                hash = record.to_hash()
                list.append(hash)
            return jsonify(list)

        # return 404 not found record does not exist
        except Place.DoesNotExist:
            return json_response(
                add_status_=False,
                status_=404,
                code=404,
                msg="not found"
            )

    # handle POST requests:
    # --------------------------------------------------------------------------
    elif request.method == 'POST':
        record = Place( owner=request.form['owner_id'],
                        city=city_id,
                        name=request.form['name'],
                        description=request.form['description'],
                        number_rooms=request.form['number_rooms'],
                        number_bathrooms=request.form['number_bathrooms'],
                        max_guest=request.form['max_guest'],
                        price_by_night=request.form['price_by_night'],
                        latitude=request.form['latitude'],
                        longitude=request.form['longitude'] )
        record.save()
        return jsonify(record.to_hash())
