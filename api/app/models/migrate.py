from base import database
from user import User
from state import State
from city import City
from place import Place
from place_book import PlaceBook
from amenity import Amenity
from place_amenity import PlaceAmenities
from review import Review
from review_user import ReviewUser
from review_place import ReviewPlace

# connect to database specified in base
database.connect()

# populate databases with tables
database.create_tables([User,
                        State,
                        City,
                        Place,
                        PlaceBook,
                        Amenity,
                        PlaceAmenities,
                        Review,
                        ReviewUser,
                        ReviewPlace], safe=True)
