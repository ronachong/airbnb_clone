from base import *
from state import State

class City(BaseModel):
    name = peewee.CharField(128, null=False, unique=True)
    state = peewee.ForeignKeyField(State, related_name="cities", on_delete='cascade')
