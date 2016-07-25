import unittest, logging
import config
import os
import json

from app import app
from app.models.user import User
from app.models.place import Place
from app.models.city import City
from app.models.state import State
from app.models.base import *
from peewee import Model
from datetime import datetime

class placeTestCase(unittest.TestCase):
    def setUp(self):
        '''
        overloads def setUp(self): to create a test client of airbnb app, and
        create Place in airbnb_test database
        '''
        self.app = app.test_client()
        self.app.testing = True
        logging.disable(logging.CRITICAL) # disable logs

        # connect to airbnb_test database and create Place table
        database.connect()
        database.create_tables([User, State, City, Place], safe=True)
        state_record = State(name='foo-state')
        state_record.save()
        city_record = City(name='foo-city', state=1)
        city_record.save()
        city_record2 = City(name='foo-city2', state=1)
        city_record2.save()

    def tearDown(self):
        '''
        tearDown removes Place from airbnb_test database upon completion of test
        case
        '''
        Place.drop_table()
        City.drop_table()
        State.drop_table()
        User.drop_table()

    def createPlaceViaPeewee(self):
        '''
        createPlaceViaPeewee creates a place record using the API's database/Peewee
        models, and returns the Peewee object for the record. This method will
        not work if the database models are not written correctly.
        '''
        record = Place( owner = 1,
                        city = 1,
                        name = "foo",
                        description = "foo description",
                        number_rooms = 1,
                        number_bathrooms = 1,
                        max_guest = 1,
                        price_by_night = 1,
                        latitude = 20.0,
                        longitude = 22.0    )
        record.save()
        return record

    def createPlaceViaAPI(self):
        '''
        createPlaceViaAPI creates a place record through a POST request to the API
        and returns the Flask response object for the request. This method will
        not work if the POST request handler is not written properly.
        '''
        POST_request = self.app.post('/places', data=dict(
            owner = 1,
            city = 1,
            name = "foo",
            description = "foo description",
            number_rooms = 1,
            number_bathrooms = 1,
            max_guest = 1,
            price_by_night = 1,
            latitude = 20.0,
            longitude = 22.0
        ))
        return POST_request

    def subtest_createWithAllParams(self):
        '''
        subtest_createWithAllParams tests proper creation of a place record upon
        a POST request to the API with all parameters provided.
        '''
        POST_request1 = self.createPlaceViaAPI()
        self.assertEqual(POST_request1.status[:3], '200')

        now = datetime.now().strftime('%d/%m/%Y %H:%M')

        self.assertEqual(Place.get(Place.id == 1).owner, 1)
        self.assertEqual(Place.get(Place.id == 1).city, 1)
        self.assertEqual(Place.get(Place.id == 1).name, "foo")
        self.assertEqual(Place.get(Place.id == 1).description, "foo description")
        self.assertEqual(Place.get(Place.id == 1).number_rooms, 1)
        self.assertEqual(Place.get(Place.id == 1).number_bathrooms, 1)
        self.assertEqual(Place.get(Place.id == 1).max_guest, 1)
        self.assertEqual(Place.get(Place.id == 1).price_by_night, 1)
        self.assertEqual(Place.get(Place.id == 1).latitude, 22.0)
        self.assertEqual(Place.get(Place.id == 1).longitude, 22.0)
        self.assertEqual(Place.get(Place.id == 1).created_at[:-3], now)
        self.assertEqual(Place.get(Place.id == 1).updated_at[:-3], now)

        # test that place ID for sole record in database is correct
        self.assertEqual(Place.select().get().id, 1)

    def subtest_createWithoutAllParams(self):
        '''
        subtest_createWithoutAllParams tests proper non-creation of a place in
        all cases of a parameter missing in a POST request to the API.
        '''
        # missing owner - should cause bad request?
        POST_request2 = self.app.post('/places', data=dict(
            city = 1,
            name = "foo",
            description = "foo description",
            number_rooms = 1,
            number_bathrooms = 1,
            max_guest = 1,
            price_by_night = 1,
            latitude = 20.0,
            longitude = 22.0
        ))

        # missing city - should cause bad request?
        POST_request3 = self.app.post('/places', data=dict(
            owner = 1,
            name = "foo",
            description = "foo description",
            number_rooms = 1,
            number_bathrooms = 1,
            max_guest = 1,
            price_by_night = 1,
            latitude = 20.0,
            longitude = 22.0
        ))

        # missing name - should cuase bad request?
        POST_request4 = self.app.post('/places', data=dict(
            owner = 1,
            city = 1,
            name = "foo",
            description = "foo description",
            number_rooms = 1,
            number_bathrooms = 1,
            max_guest = 1,
            price_by_night = 1,
            latitude = 20.0,
            longitude = 22.0
        ))

        # missing description - should cause bad request?
        POST_request5 = self.app.post('/places', data=dict(
            owner = 1,
            city = 1,
            name = "foo",
            description = "foo description",
            number_rooms = 1,
            number_bathrooms = 1,
            max_guest = 1,
            price_by_night = 1,
            latitude = 20.0,
            longitude = 22.0
        ))

        # missing number of rooms - should be OK due to default val of 0?
        POST_request6 = self.app.post('/places', data=dict(
            owner = 1,
            city = 1,
            name = "foo",
            description = "foo description",
            number_rooms = 1,
            number_bathrooms = 1,
            max_guest = 1,
            price_by_night = 1,
            latitude = 20.0,
            longitude = 22.0
        ))

        # missing number of bathrooms - should be OK due to default val of 0?
        POST_request7 = self.app.post('/places', data=dict(
            owner = 1,
            city = 1,
            name = "foo",
            description = "foo description",
            number_rooms = 1,
            number_bathrooms = 1,
            max_guest = 1,
            price_by_night = 1,
            latitude = 20.0,
            longitude = 22.0
        ))

        # missing max_guest - should be OK due to default val of 0?
        POST_request8 = self.app.post('/places', data=dict(
            owner = 1,
            city = 1,
            name = "foo",
            description = "foo description",
            number_rooms = 1,
            number_bathrooms = 1,
            max_guest = 1,
            price_by_night = 1,
            latitude = 20.0,
            longitude = 22.0
        ))

        # missing price_by_night - should be OK due to default val of 0?
        POST_request9 = self.app.post('/places', data=dict(
            owner = 1,
            city = 1,
            name = "foo",
            description = "foo description",
            number_rooms = 1,
            number_bathrooms = 1,
            max_guest = 1,
            price_by_night = 1,
            latitude = 20.0,
            longitude = 22.0
        ))

        # missing latitude - should cause bad request?
        POST_request10 = self.app.post('/places', data=dict(
            owner = 1,
            city = 1,
            name = "foo",
            description = "foo description",
            number_rooms = 1,
            number_bathrooms = 1,
            max_guest = 1,
            price_by_night = 1,
            latitude = 20.0,
            longitude = 22.0
        ))

        # missing longitude - should cause bad request?
        POST_request11 = self.app.post('/places', data=dict(
            owner = 1,
            city = 1,
            name = "foo",
            description = "foo description",
            number_rooms = 1,
            number_bathrooms = 1,
            max_guest = 1,
            price_by_night = 1,
            latitude = 20.0,
            longitude = 22.0
        ))

        for request in [POST_request2, POST_request3, POST_request4,
                        POST_request5, POST_request10, POST_request11]:
            self.assertEqual(request.status[:3], '400')

        for request in [POST_request6, POST_request7, POST_request8,
                        POST_request9]:
            self.assertEqual(request.status[:3], '200')

    def test_create(self):
        '''
        test_create tests proper creation (or non-creation) of place records upon
        POST requests to API
        '''
        # test creation of place with all parameters provided in POST request
        self.subtest_createWithAllParams()

        # test creation of place in all cases of a parameter missing in POST request
        self.subtest_createWithoutAllParams()

    def test_list(self):
        '''
        test_list tests proper representation of all place records upon GET
        requests to API
        '''
        # delete and recreate Place table for test
        Place.drop_table()
        database.create_tables([Place], safe=True)

        GET_request1 = self.app.get('/places')
        self.assertEqual(len(json.loads(GET_request1.data)), 0)

        self.createPlaceViaPeewee()

        GET_request2 = self.app.get('/places')
        self.assertEqual(len(json.loads(GET_request2.data)), 1)

    def test_get(self):
        '''
        test_get tests proper representation of a place record upon GET requests
        via place ID to API
        '''
        # delete and recreate Place table for test
        Place.drop_table()
        database.create_tables([Place], safe=True)

        # test response of GET request for place by place id
        self.createPlaceViaPeewee()

        GET_request1 = self.app.get('/places/1')
        GET_data = json.dumps(GET_request1.data)
        self.assertEqual(GET_request1.status[:3], '200')

        self.assertEqual(Place.get(Place.id == 1).email, GET_data[0]['owner'])
        self.assertEqual(Place.get(Place.id == 1).password, GET_data[0]['city'])
        self.assertEqual(Place.get(Place.id == 1).first_name, GET_data[0]['name'])
        self.assertEqual(Place.get(Place.id == 1).description, GET_data[0]['description'])
        self.assertEqual(Place.get(Place.id == 1).number_rooms, GET_data[0]['number_rooms'])
        self.assertEqual(Place.get(Place.id == 1).number_bathrooms, GET_data[0]['number_bathrooms'])
        self.assertEqual(Place.get(Place.id == 1).max_guest, GET_data[0]['max_guest'])
        self.assertEqual(Place.get(Place.id == 1).price_by_night, GET_data[0]['price_by_night'])
        self.assertEqual(Place.get(Place.id == 1).latitude, GET_data[0]['latitude'])
        self.assertEqual(Place.get(Place.id == 1).longitude, GET_data[0]['longitude'])
        self.assertEqual(Place.get(Place.id == 1).created_at, GET_data[0]['created_at'])
        self.assertEqual(Place.get(Place.id == 1).updated_at, GET_data[0]['updated_at'])

        # test response of GET request for place by place id which does not exist
        GET_request2 = self.app.get('/places/1000')
        self.assertEqual(GET_request2.status[:3], '404')

    def test_delete(self):
        '''
        test_delete tests deletion of place records upon DELETE requests to API
        '''
        # delete and recreate Place table for test
        Place.drop_table()
        database.create_tables([Place], safe=True)

        # test response of DELETE request for place by place id
        self.createPlaceViaPeewee()

        GET_request1 = self.app.get('/places')

        DELETE_request1 = self.app.delete('/places/1')

        GET_request2 = self.app.get('/places')

        num_records_b4 = len(json.loads(GET_request1.data))
        num_records_after = len(json.loads(GET_request2.data))

        self.assertEqual(DELETE_request1.status[:3], '200')
        self.assertEqual(num_records_after, num_records_b4 - 1)

        # test response of DELETE request for place by place id which does not exist
        DELETE_request2 = self.app.delete('/places/1000')
        self.assertEqual(DELETE_request2.status[:3], '404')

    def test_update(self):
        '''
        test_update tests update of place records upon PUT requests to API
        '''
        # delete and recreate Place table for test
        Place.drop_table()
        database.create_tables([Place], safe=True)

        self.createPlaceViaPeewee()

        PUT_request1 = self.app.put('/places/1', data=dict(
            name = "foo-name2",
            description = "foo description 2",
            number_rooms = 2,
            number_bathrooms = 2,
            max_guest = 2,
            price_by_night = 2,
            latitude = 30.0,
            longitude = 32.0
        ))
        self.assertEqual(PUT_request1.status[:3], '200')

        self.assertEqual(Place.get(Place.id == 1).name, 'foo-name2')
        self.assertEqual(Place.get(Place.id == 1).description, 'foo description 2')
        self.assertEqual(Place.get(Place.id == 1).number_rooms, 2)
        self.assertEqual(Place.get(Place.id == 1).number_bathrooms, 2)
        self.assertEqual(Place.get(Place.id == 1).max_guest, 2)
        self.assertEqual(Place.get(Place.id == 1).price_by_night, 2)
        self.assertEqual(Place.get(Place.id == 1).latitude, 30.0)
        self.assertEqual(Place.get(Place.id == 1).longitude, 32.0)

        # test response of PUT request for place by place id which does not exist
        PUT_request2 = self.app.put('/places/1000')
        self.assertEqual(PUT_request2.status[:3], '404')

    def test_createByCity(self):
        '''
        test_createByCity tests proper creation of a place record by city upon
        POST request to API
        '''
        # delete and recreate Place table for test
        Place.drop_table()
        database.create_tables([Place], safe=True)

        POST_request = self.app.post('/states/1/cities/1/places', data=dict(
            owner = 1,
            name = "foo",
            description = "foo description",
            number_rooms = 1,
            number_bathrooms = 1,
            max_guest = 1,
            price_by_night = 1,
            latitude = 20.0,
            longitude = 22.0
        ))

        self.assertEqual(Place.get(Place.id == 1).city, 1)

    def test_getByCity(self):
        '''
        test_getByCity tests proper representation of all place records by city
        upon GET requests to API
        '''
        # delete and recreate Place table for test
        Place.drop_table()
        database.create_tables([Place], safe=True)

        GET_request1 = self.app.get('/states/1/cities/1/places')
        self.assertEqual(len(json.loads(GET_request1.data)), 0)

        POST_request = self.app.post('/states/1/cities/1/places', data=dict(
            owner = 1,
            name = "foo",
            description = "foo description",
            number_rooms = 1,
            number_bathrooms = 1,
            max_guest = 1,
            price_by_night = 1,
            latitude = 20.0,
            longitude = 22.0
        ))

        GET_request2 = self.app.get('/states/1/cities/1/places')
        self.assertEqual(len(json.loads(GET_request2.data)), 1)

        POST_request = self.app.post('/states/1/cities/2/places', data=dict(
            owner = 1,
            name = "foo",
            description = "foo description",
            number_rooms = 1,
            number_bathrooms = 1,
            max_guest = 1,
            price_by_night = 1,
            latitude = 20.0,
            longitude = 22.0
        ))

        GET_request3 = self.app.get('/states/1/cities/1/places')
        self.assertEqual(len(json.loads(GET_request3.data)), 1)
