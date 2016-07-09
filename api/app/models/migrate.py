from base import database
from user, state, city, place, place_book, amenity, place_amenity import *

# connect to database specified in base
database.connect()

# populate databases with tables
database.create_tables([User, State, City, Place, PlaceBook, Amenity, PlaceAmenities], safe=True)
