import peewee

from place import Place
from review import Review
from base import *


class ReviewPlace(peewee.Model):
    place = peewee.ForeignKeyField(Place)
    review = peewee.ForeignKeyField(Review)

    class Meta:
        database = database
