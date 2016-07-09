from peewee import Model, ManyToManyField

class PlaceAmenities(peewee.Model):
    place = peewee.ManyToManyField(Place)
    amenity = peewee.ManyToManyField(Amenity)
