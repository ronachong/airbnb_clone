from peewee import Model
from playhouse.fields import ManyToManyField
from place import Place
from amenity import Amenity
from base import database

class PlaceAmenities(Model):
    place = ManyToManyField(Place)
    amenity = ManyToManyField(Amenity)

    class Meta:
        database = database
        order_by = ("id", ) # what is the extra space for?
