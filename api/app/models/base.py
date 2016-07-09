import peewee
from config import *

'''
base.py defines the database variable that Peewee will use to access the clone's MySQL database.
base.py also defines a basemodel for all the classes that will be used by Peewee to create and access the database tables.
'''

database = MySQLDatabase( DATABASE['database'],
                          user=DATABASE['user'],
                          charset=DATABASE['charset'],
                          host=DATABASE['host'],
                          port=DATABASE['3306'],
                          passwd=DATABASE['password'] )

class BaseModel(peewee.Model):
    id = peewee.PrimaryKeyField(unique=True)
    created_at = peewee.DateTimeField(default=datetime.datetime.now, formats='%Y/%m/%d %H:%M:%S') # peewee docs have datetime.datetime.now in exp; might have to check if format comes out right
    updated_at = peewee.DateTimeField(default=datetime.datetime.now, formats='%Y/%m/%d %H:%M:%S')


    
    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now
        peewee.Model.save() # not sure if this goes before or after self.updated_at assignment    

    class Meta:
        database = database
        order_by = ("id", ) # what is the extra space for?
