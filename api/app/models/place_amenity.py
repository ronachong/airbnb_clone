from peewee import Model
from playhouse.fields import ManyToManyField
from place import Place
from amenity import Amenity

class PlaceAmenities(Model):
    place = ManyToManyField(Place)
    amenity = ManyToManyField(Amenity)
