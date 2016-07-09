from base import *

class City(BaseModel):
    name = CharField(128, null=False, unique=True)
    state = ForeignKeyField(State, related_name="cities", cascade=True)
