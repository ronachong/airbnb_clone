from base import *
from place import Place
from user import User

class PlaceBook(BaseModel):
    place = peewee.ForeignKeyField(Place)
    user = peewee.ForeignKeyField(User, related_name="places_booked")
    is_validated = peewee.BooleanField(default=False)
    date_start = peewee.DateTimeField(null=False, formats='%d/%m/%Y %H:%M:%S')
    number_nights = peewee.IntegerField(default=1)

    def to_hash(self):
        hash = {}
        hash["id"] = self.id
        hash["created_at"] = self.created_at.strftime('%d/%m/%Y %H:%M:%S')
        hash["updated_at"] = self.updated_at.strftime('%d/%m/%Y %H:%M:%S')
        hash["place_id"] = self.place.id
        hash["user_id"] = self.user.id
        hash["is_validated"] = self.is_validated
        hash["date_start"] = self.date_start.strftime('%d/%m/%Y %H:%M:%S')
        hash["number_nights"] = self.number_nights
        return hash
