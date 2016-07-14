from base import *
from state import State

class City(BaseModel):
    name = peewee.CharField(128, null=False, unique=True)
    state = peewee.ForeignKeyField(State, related_name="cities", on_delete='cascade')

    def to_hash(self):
        hash = {}
        hash["id"] = self.id
        hash["created_at"] = self.created_at.strftime('%d/%m/%Y %H:%M:%S')
        hash["updated_at"] = self.updated_at.strftime('%d/%m/%Y %H:%M:%S')
        hash["name"] = self.name
        hash["state_id"] = self.state.id
        return hash
