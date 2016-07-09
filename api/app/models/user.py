from base import *
import hashlib

class User(BaseModel):
    email = CharField(128, null=False, unique=True)
    password = CharField(128, null=False)
    first_name = CharField(128, null=False)
    last_name = CharField(128, null=False)
    is_admin = BooleanField(default=False)

    def set_password(self, clear_password):
        m = hashlib.md5()
        m.update(self.clear_password)
        self.password = m.digest()
