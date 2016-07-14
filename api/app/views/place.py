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
                        max_guest=place_mguests,
                        price_by_night=place_pbn,
                        latitude=place_lat,
                        longitude=place_long )
        record.save()
        return jsonify(record.to_hash())

# @app.route('/states/<state_id>/cities/<city_id>', methods=['GET','DELETE'])
# def city_id(state_id, city_id):
#     ''' '''
#     record = City.get(City.id == city_id)
#
#     if request.method == 'GET':
#         return jsonify(record.to_hash())
#
#     elif request.method == "DELETE":
#         record.delete_instance()
#         record.save()
#         return 'deleted city\n'
