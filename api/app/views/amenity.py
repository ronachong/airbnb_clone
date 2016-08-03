from flask import jsonify, request
from flask_json import json_response
from peewee import *

from app.models.amenity import Amenity
from app.models.place_amenity import PlaceAmenities
from app.models.place import Place
from app import app


@app.route('/amenities', methods=['GET','POST'])
def amenities():
    """Handle GET and POST requests to /amenities route.

    Return a list of all amenities in database in the case of a GET request.
    Create a new amenity record in the database in the case of a POST request.
    """
    # handle GET requests:
    # --------------------------------------------------------------------------
    if request.method == 'GET':
        list = []
        for record in Amenity.select():
            hash = record.to_hash()
            list.append(hash)
        return jsonify(list)

    # handle POST requests:
    # --------------------------------------------------------------------------
    elif request.method == 'POST':
        try:
            record = Amenity(name=request.form['name'])
            record.save()
            return jsonify(record.to_hash())

        # return 409 if amenity with given name already exists
        except IntegrityError:
                return json_response(
                    add_status_=False,
                    status_=409,
                    code=10003,
                    msg="Name already exists"
                )


@app.route('/amenities/<amenity_id>', methods=['GET', 'DELETE'])
def amenity_id(amenity_id):
    """Handle GET, PUT & DELETE requests to /amenities/<amenity_id> route.

    Return a hash of the appropriate record in the case of a GET request.
    Delete appropriate record in case of DELETE request.
    """
    # check whether resource exists:
    # --------------------------------------------------------------------------
    try:
        record = Amenity.get(Amenity.id == amenity_id)

    # return 404 not found if it does not
    except Amenity.DoesNotExist:
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
    elif request.method == "DELETE":
        record.delete_instance()
        record.save()
        return 'deleted booking\n'


@app.route('/places/<place_id>/amenities', methods=['GET'])
def place_amenities(place_id):
    # need to test and correct this request handler
    query = (Amenity
                .select()
                .join(PlaceAmenities, on=(Amenity.id == PlaceAmenities.amenity))
                .join(Place, on=(Place.id == PlaceAmenities.place))
                .where(Place.id == place_id)
                .get())

    for record in query:
        hash = record.to_hash()
        list.append(hash)
    return jsonify(list)
