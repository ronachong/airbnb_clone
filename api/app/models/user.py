from base import *
import hashlib

class User(BaseModel):
    email = peewee.CharField(128, null=False, unique=True)
    password = peewee.CharField(128, null=False)
    first_name = peewee.CharField(128, null=False)
    last_name = peewee.CharField(128, null=False)
    is_admin = peewee.BooleanField(default=False)

    '''
    def __init__(attribute1=args1, args2, args3):
        self.attribute1 = args1
        self.email = args2
        self.password = args3
    '''

    def set_password(self, clear_password):
        m = hashlib.md5()
        m.update(self.clear_password)
        self.password = m.digest()

    def to_hash(self):
        hash = {}
        hash["id"] = self.id
        hash["created_at"] = self.created_at.strftime('%d/%m/%Y %H:%M:%S')
        hash["updated_at"] = self.updated_at.strftime('%d/%m/%Y %H:%M:%S')
        hash["email"] = self.email
        hash["first_name"] = self.first_name
        hash["last_name"] = self.last_name
        hash["is_admin"] = self.is_admin
        return hash
