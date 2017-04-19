from datetime import datetime

from flask import jsonify, request
from flask_json import json_response
from peewee import *

from app.views.return_styles import ListStyle
from app.models.place_book import PlaceBook
from app import app


@app.route('/places/<place_id>/books', methods=['GET', 'POST'])
def books(place_id):
    """Handle GET and POST requests to /places/<place_id>/books route.

    Return a list of all bookings in database in the case of a GET request.
    Create a new placebook record in the database in the case of a POST request.
    """
    # handle GET requests:
    # --------------------------------------------------------------------------
    if request.method == 'GET':
        list = ListStyle.list(
            PlaceBook.select().where(PlaceBook.place == place_id),
            request
        )
        return jsonify(list)

    # handle POST requests:
    # --------------------------------------------------------------------------
    elif request.method == 'POST':
        record = PlaceBook(
            place=request.form['place'],
            user=request.form['user'],
            is_validated=request.form['is_validated'],
            date_start=datetime.strptime(
                request.form['date_start'],
                '%d/%m/%Y %H:%M:%S'
                ),
            number_nights=request.form['number_nights']
        )
        record.save()
        return jsonify(record.to_hash())


@app.route('/places/<place_id>/books/<book_id>', methods=['GET', 'PUT', 'DELETE'])
def book_id(place_id, book_id):
    """Handle GET, PUT & DELETE requests to /places/<place_id>/books/<book_id>.

    Return a hash of the appropriate record in the case of a GET request.
    Update appropriate hash in database in case of PUT request.
    Delete appropriate record in case of DELETE request.
    """
    # check whether resource exists:
    # --------------------------------------------------------------------------
    try:
        record = PlaceBook.get(PlaceBook.id == book_id)

    except PlaceBook.DoesNotExist:
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

    # handle DELETE requests
    elif request.method == "DELETE":
        record.delete_instance()
        record.save()
        return 'deleted booking\n'
