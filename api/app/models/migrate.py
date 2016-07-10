from base import database
from user import User
from state import State
from city import City
from place import Place
from place_book import PlaceBook
from amenity import Amenity
from place_amenity import PlaceAmenities

# connect to database specified in base
database.connect()

# populate databases with tables
database.create_tables([User, State, City, Place, PlaceBook, Amenity, PlaceAmenities], safe=True)

# create a test entry
test_record=User(email='foo', password='foo', first_name='foo',last_name='foo')
test_record.save()
