from flask import jsonify, request
from flask_json import json_response
from datetime import datetime
from app.models.place_book import PlaceBook
from app import app
from peewee import *

@app.route('/places/<place_id>/books', methods=['GET','POST'])
def books(place_id):
    ''' books returns a list of all books in the database with the given id in the case of a GET request, and creates a new place in the database in the case of a POST request '''
    if request.method == 'GET':
        list = []
        for record in PlaceBook.select().where(PlaceBook.place == place_id):
            hash = record.to_hash()
            list.append(hash)
        return jsonify(list)

    elif request.method == 'POST':
        record = PlaceBook (place = request.form['place'],
                            user = request.form['user'],
                            is_validated = request.form['is_validated'],
                            date_start = datetime.strptime(request.form['date_start'], '%d/%m/%Y %H:%M:%S'),
                            number_nights = request.form['number_nights'] )

        record.save()
        return jsonify(record.to_hash())

@app.route('/places/<place_id>/books/<book_id>', methods=['GET', 'PUT', 'DELETE'])
def book_id(place_id, book_id):
    '''  '''
    record = PlaceBook.get(PlaceBook.id == book_id)

    if request.method == 'GET':
        return jsonify(record.to_hash())

    elif request.method == 'PUT':
        # code below can be optimized in future using list comprehensions
        for key in request.values.keys():
            if key == "place":
                record.place = request.values[key]
            elif key == "user":
                record.user = request.values[key]
            elif key == "is_validated":
                record.is_validated = request.values[key]
            elif key == "date_start":
                record.date_start = request.values[key]
            elif key == "number_nights":
                record.number_nights = request.values[key]
            record.save()
        return jsonify(record.to_hash())

    elif request.method == "DELETE":
        record.delete_instance()
        record.save()
        return 'deleted booking\n'
