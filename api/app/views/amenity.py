from flask import jsonify, request
from flask_json import json_response
from app.models.amenity import Amenity
from app.models.place_amenity import PlaceAmenities
from app.models.place import Place
from app import app
from peewee import *

@app.route('/amenities', methods=['GET','POST'])
def amenities():
    ''' amenities returns a list of all amenity records in the database in the case of a GET request, and creates a new amenity record in the database in the case of a POST request '''
    if request.method == 'GET':
        list = []
        for record in Amenity.select():
            hash = record.to_hash()
            list.append(hash)
        return jsonify(list)

    elif request.method == 'POST':
        try:
            record = Amenity( name = request.form['name'] )
            record.save()
            return jsonify(record.to_hash())
        except:
            return json_response(add_status_=False, status_=409, code=10003, msg="Name already exists")


@app.route('/amenities/<amenity_id>', methods=['GET', 'DELETE'])
def amenity_id(amenity_id):
    '''  '''
    record = Amenity.get(Amenity.id == amenity_id)

    if request.method == 'GET':
        return jsonify(record.to_hash())

    elif request.method == "DELETE":
        record.delete_instance()
        record.save()
        return 'deleted booking\n'

@app.route('/places/<place_id>/amenities', methods=['GET'])
def place_amenities(place_id):
    #return 'Haven\'t figured this part out yet :D'
    query = ( Amenity
                .select()
                .join(PlaceAmenities, on=(Amenity.id == PlaceAmenities.amenity))
                .join(Place, on=(Place.id == PlaceAmenities.place))
                .where(Place.id == place_id)
                .get() )

    for record in query:
        hash = record.to_hash()
        list.append(hash)
    return jsonify(list)
