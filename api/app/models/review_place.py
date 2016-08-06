import peewee

from app.models.place import Place
from app.models.review import Review
from app.models import base


class ReviewUser(peewee.Model):
    place = peewee.ForeignKeyField(Place)
    review = peewee.ForeignKeyField(Review)

    class Meta:
        database = base.database
