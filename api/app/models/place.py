from base import *
from user import User
from city import City

class Place(BaseModel):
    owner = peewee.ForeignKeyField(User, related_name="places")
    city = peewee.ForeignKeyField(City, related_name="places")
    name = peewee.CharField(128, null=False)
    description = peewee.TextField()
    number_rooms = peewee.IntegerField(default=0)
    number_bathrooms = peewee.IntegerField(default=0)
    max_guest = peewee.IntegerField(default=0)
    price_by_night = peewee.IntegerField(default=0)
    latitude = peewee.FloatField()
    longitude = peewee.FloatField()

    def to_hash(self):
        hash = {}
        hash["id"] = self.id
        hash["created_at"] = self.created_at.strftime('%d/%m/%Y %H:%M:%S')
        hash["updated_at"] = self.updated_at.strftime('%d/%m/%Y %H:%M:%S')
        hash["owner_id"] = self.owner.id
        hash["city_id"] = self.city.id
        hash["name"] = self.name
        hash["description"] = self.description
        hash["number_rooms"] = self.number_rooms
        hash["number_bathrooms"] = self.number_bathrooms
        hash["max_guest"] = self.max_guest
        hash["price_by_night"] = self.price_by_night
        hash["latitude"] = self.latitude
        hash["longitude"] = self.longitude
        return hash
