import unittest, logging
import config
import os
import json

from app import app
from app.models.user import User
from app.models.state import State
from app.models.city import City
from app.models.place import Place
from app.models.place_book import PlaceBook
from app.models.base import *
from peewee import Model
from datetime import datetime

class placebookTestCase(unittest.TestCase):
    def setUp(self):
        '''
        overloads def setUp(self): to create a test client of airbnb app, and
        create PlaceBook in airbnb_test database
        '''
        self.app = app.test_client()
        self.app.testing = True
        logging.disable(logging.CRITICAL) # disable logs

        # connect to airbnb_test database and create PlaceBook table
        db.connect()
        db.create_tables([User, State, City, Place, PlaceBook], safe=True)
        user_record = User( email='anystring',
                            password='anystring1',
                            first_name='anystring2',
                            last_name='anystring3'  )
        user_record.save()
        state_record = State(name="foo-state")
        state_record.save()
        city_record = City(name="foo-city", state="1")
        city_record.save()
        place_record = Place(   owner = 1,
                                city = 1,
                                name = "foo",
                                description = "foo description",
                                number_rooms = 1,
                                number_bathrooms = 1,
                                max_guest = 1,
                                price_by_night = 1,
                                latitude = 20.0,
                                longitude = 22.0    )
        place_record.save()
        place_record2 = Place(  owner = 1,
                                city = 1,
                                name = "foo",
                                description = "foo description",
                                number_rooms = 1,
                                number_bathrooms = 1,
                                max_guest = 1,
                                price_by_night = 1,
                                latitude = 20.0,
                                longitude = 22.0    )
        place_record2.save()

    def tearDown(self):
        '''
        tearDown removes PlaceBook from airbnb_test database upon completion of test
        case
        '''
        User.drop_table()
        PlaceBook.drop_table()
        Place.drop_table()
        City.drop_table()
        State.drop_table()

    def createPlaceBookViaPeewee(self):
        '''
        createPlaceBookViaPeewee creates a placebook record using the API's database/Peewee
        models, and returns the Peewee object for the record. This method will
        not work if the database models are not written correctly.
        '''
        record = PlaceBook(     user_id=1,
                                is_validated=False,
                                date_start=datetime.now().strftime('%d/%m/%Y %H:%M'),
                                number_nights=1 )
        record.save()
        return record

    def createPlaceBookViaAPI(self):
        '''
        createPlaceBookViaAPI creates a user record through a POST request to the API
        and returns the Flask response object for the request. This method will
        not work if the POST request handler is not written properly.
        '''
        POST_request = self.app.post('/places/1/books', data=dict(
            user_id=1,
            is_validated=False,
            date_start=datetime.now().strftime('%d/%m/%Y %H:%M'),
            number_nights=1
        ))
        return POST_request

    def subtest_createWithAllParams(self):
        '''
        subtest_createWithAllParams tests proper creation of a user record upon
        a POST request to the API with all parameters provided.
        '''
        POST_request1 = self.createPlaceBookViaAPI()
        self.assertEqual(POST_request1.status[:3], '200')

        now = datetime.now().strftime('%d/%m/%Y %H:%M')

        self.assertEqual(PlaceBook.get(PlaceBook.id == 1).place_id, 1)
        self.assertEqual(PlaceBook.get(PlaceBook.id == 1).user_id, 1)
        self.assertEqual(PlaceBook.get(PlaceBook.id == 1).is_validated, False)
        self.assertEqual(PlaceBook.get(PlaceBook.id == 1).date_start, datetime.now().strftime('%d/%m/%Y %H:%M'))
        self.assertEqual(PlaceBook.get(PlaceBook.id == 1).number_nights, 1)
        self.assertEqual(PlaceBook.get(PlaceBook.id == 1).created_at[:-3], now)
        self.assertEqual(PlaceBook.get(PlaceBook.id == 1).updated_at[:-3], now)

        # test that placebook ID for sole record in database is correct
        self.assertEqual(PlaceBook.select().get().id, 1)

    def subtest_createWithoutAllParams(self):
        '''
        subtest_createWithoutAllParams tests proper non-creation of a place_book in
        all cases of a parameter missing in a POST request to the API.
        '''
        # user_id missing - request should fail due to no default value
        POST_request2 = self.app.post('/places/1/books', data=dict(
            is_validated=1,
            date_start=datetime.now().strftime('%d/%m/%Y %H:%M'),
            number_nights=1
        ))

        # is_validated missing - request shouldn't fail due to default value False
        POST_request3 = self.app.post('/places/1/books', data=dict(
            user_id=1,
            date_start=datetime.now().strftime('%d/%m/%Y %H:%M'),
            number_nights=1
        ))

        # date_start missing - request should fail due to no default value
        POST_request4 = self.app.post('/places/1/books', data=dict(
            user_id=1,
            is_validated=False,
            number_nights=1
        ))

        # number_nights missing - request shouldn't fail due to default value 1
        POST_request5 = self.app.post('/places/1/books', data=dict(
            user_id=1,
            is_validated=False,
            date_start=datetime.now().strftime('%d/%m/%Y %H:%M')
        ))

        for request in [POST_request2, POST_request4]:
            self.assertEqual(request.status[:3], '400')

        for request in [POST_request5, POST_request3]:
            self.assertEqual(request.status[:3], '200')

        # could write queries to check if supposedly successful records have
        # proper default values

    def test_create(self):
        '''
        test_create tests proper creation (or non-creation) of place_book records upon
        POST requests to API
        '''
        # test creation of place_book with all parameters provided in POST request
        self.subtest_createWithAllParams()

        # test creation of place_book in all cases of a parameter missing in POST request
        self.subtest_createWithoutAllParams()

    def test_list(self):
        '''
        test_list tests proper representation of all place_book records upon GET
        requests to API
        '''
        # delete and recreate PlaceBook table for test
        PlaceBook.drop_table()
        db.create_tables([PlaceBook], safe=True)

        GET_request1 = self.app.get('/places/1/books')
        self.assertEqual(len(json.loads(GET_request1.data)), 0)

        self.createPlaceBookViaPeewee()

        GET_request2 = self.app.get('/places/1/books')
        self.assertEqual(len(json.loads(GET_request2.data)), 1)

        # could also test to make sure records returned only belong to respect-
        # ive place

    def test_get(self):
        '''
        test_get tests proper representation of a place_book record upon GET requests
        via book ID to API
        '''
        # delete and recreate PlaceBook table for test
        PlaceBook.drop_table()
        db.create_tables([PlaceBook], safe=True)

        # test response of GET request for placebook by placebook id
        self.createPlaceBookViaPeewee()

        GET_request1 = self.app.get('/places/1/books/1')
        GET_data = json.dumps(GET_request1.data)
        self.assertEqual(GET_request1.status[:3], '200')

        self.assertEqual(PlaceBook.get(PlaceBook.id == 1).place_id, GET_data[0]['place_id'])
        self.assertEqual(PlaceBook.get(PlaceBook.id == 1).user_id, GET_data[0]['user_id'])
        self.assertEqual(PlaceBook.get(PlaceBook.id == 1).is_validated, GET_data[0]['is_validated'])
        self.assertEqual(PlaceBook.get(PlaceBook.id == 1).date_start, GET_data[0]['date_start'])
        self.assertEqual(PlaceBook.get(PlaceBook.id == 1).number_nights, GET_data[0][1])
        self.assertEqual(PlaceBook.get(PlaceBook.id == 1).created_at, GET_data[0]['created_at'])
        self.assertEqual(PlaceBook.get(PlaceBook.id == 1).updated_at, GET_data[0]['updated_at'])

        # test response of GET request for booking by booking id which does not exist
        GET_request2 = self.app.get('places/1/books/1000')
        self.assertEqual(GET_request2.status[:3], '404')

    def test_delete(self):
        '''
        test_delete tests deletion of place_book records upon DELETE requests to API
        '''
        # delete and recreate PlaceBook table for test
        PlaceBook.drop_table()
        db.create_tables([PlaceBook], safe=True)

        # test response of DELETE request for place_book by place_book id
        self.createPlaceBookViaPeewee()

        GET_request1 = self.app.get('/places/1/books')

        DELETE_request1 = self.app.delete('places/1/books/1')

        GET_request2 = self.app.get('/places/1/books')

        num_records_b4 = len(json.loads(GET_request1.data))
        num_records_after = len(json.loads(GET_request2.data))

        self.assertEqual(DELETE_request1.status[:3], '200')
        self.assertEqual(num_records_after, num_records_b4 - 1)

        # test response of DELETE request for place_book by place_book id which does not exist
        DELETE_request2 = self.app.delete('/places/1/books/1000')
        self.assertEqual(DELETE_request2.status[:3], '404')

    def test_update(self):
        '''
        test_update tests update of place_book records upon PUT requests to API
        '''
        # delete and recreate PlaceBook table for test
        PlaceBook.drop_table()
        db.create_tables([PlaceBook], safe=True)

        self.createPlaceBookViaPeewee()

        PUT_request1 = self.app.put('places/1/books/1', data=dict(
            place_id=2,
            is_validated=True,
            date_start=datetime.now().strftime('%d/%m/%Y %H:%M'),
            number_nights=3
        ))
        self.assertEqual(PUT_request1.status[:3], '200')

        self.assertEqual(PlaceBook.get(PlaceBook.id == 1).place_id, 2)
        self.assertEqual(PlaceBook.get(PlaceBook.id == 1).is_validated, True)
        self.assertEqual(PlaceBook.get(PlaceBook.id == 1).date_start, datetime.now().strftime('%d/%m/%Y %H:%M'))
        self.assertEqual(PlaceBook.get(PlaceBook.id == 1).number_nights, 3)

        # test response of PUT request for user by user id which does not exist
        PUT_request2 = self.app.put('places/1/books/1000')
        self.assertEqual(PUT_request2.status[:3], '404')
