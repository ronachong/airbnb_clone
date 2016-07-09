from peewee import Model

class PlaceAmenities(peewee.Model):
    place = ManyToManyField(Place)
    amenity = ManyToManyField(Amenity)
