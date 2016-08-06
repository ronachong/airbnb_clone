import peewee

from app.models.user import User
from app.models.review import Review
from app.models import base


class ReviewUser(peewee.Model):
    user = peewee.ForeignKeyField(User)
    review = peewee.ForeignKeyField(Review)

    class Meta:
        database = base.database
