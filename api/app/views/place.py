from flask import jsonify, request
from flask_json import json_response
from app.models.place import Place
from app import app
from peewee import *

@app.route('/places', methods=['GET','POST'])
def places():
    ''' places returns a list of all cities in the database in the case of a GET request, and creates a new place in the database in the case of a POST request '''
    if request.method == 'GET':
        list = []
        for record in Place.select():
            hash = record.to_hash()
            list.append(hash)
        return jsonify(list)

    elif request.method == 'POST':
        place_owner = request.form['user_id']
        place_city = request.form['city_id']
        place_name = request.form['name']
        place_desc = request.form['description']
        nb_rooms = request.form['number_rooms']
        nb_bathrooms = request.form['number_bathrooms']
        place_mguests = request.form['max_guest']
        place_pbn = request.form['price_by_night']
        place_lat = request.form['latitude']
        place_long = request.form['longitude']

        record = Place( owner=place_owner,
                        city=place_city,
                        name=place_name,
                        description=place_desc,
                        number_rooms=nb_rooms,
                        number_bathrooms=nb_bathrooms,
                        max_guest=place_mguests,
                        price_by_night=place_pbn,
                        latitude=place_lat,
                        longitude=place_long )
        record.save()
        return jsonify(record.to_hash())

@app.route('/places/<place_id>', methods=['GET', 'PUT', 'DELETE'])
def place_id(place_id):
    '''  '''
    record = Place.get(Place.id == place_id)

    if request.method == 'GET':
        return jsonify(record.to_hash())

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

    elif request.method == "DELETE":
        record.delete_instance()
        record.save()
        return 'deleted city\n'
