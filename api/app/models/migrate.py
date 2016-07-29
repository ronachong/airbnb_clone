from base import database
from user import User
from state import State
from city import City
from place import Place
from place_book import PlaceBook
from amenity import Amenity
from place_amenity import PlaceAmenities
from peewee import Model
from flask import jsonify

# connect to database specified in base
database.connect()

# populate databases with tables
database.create_tables([User, State, City, Place, PlaceBook, Amenity, PlaceAmenities], safe=True)

# create a test entry
#for record in User.select():
#    record.delete_instance()
#    record.save

# for record in User.select():
#     print record.to_hash()

# test_record=User(email='foo9', password='foo', first_name='foo',last_name='foo')
# print test_record.created_at
# test_record.save()
# print test_record.to_hash()

# state_record = State(name="test7")
# state_record.save()
# print state_record.to_hash()

# city_record = City(name="testname2", state=3)
# city_record.save()
# print jsonify(city_record.to_hash())

# for city in State.get(State.id == 3).cities:
#     print city.name

# record = Place( owner='foo',
#                 city=3,
#                 name=place_name,
#                 description=place_desc,
#                 number_rooms=nb_rooms,
#                 max_guest=place_mguests,
#                 price_by_night=place_pbn,
#                 latitude=place_lat,
#                 longitude=place_long )
# record.save()

# record = Amenity( name = 'name' )
# record.save()
# print record.to_hash()
