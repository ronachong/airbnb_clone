import peewee

from user import User
from review import Review
from base import *


class ReviewUser(peewee.Model):
    user = peewee.ForeignKeyField(User)
    review = peewee.ForeignKeyField(Review)

    class Meta:
        database = database
