import logging
import json
import unittest
from datetime import datetime

from peewee import Model

from app import app
from app.views import city, state
from app.models.city import City
from app.models.state import State
from app.models.base import database


class cityTestCase(unittest.TestCase):
    def setUp(self):
        """
        Overload def setUp(self): to create a test client of airbnb app, and
        create city table in airbnb_test database.
        """
        self.app = app.test_client()        # set up test client
        self.app.testing = True             # set testing to True
        logging.disable(logging.CRITICAL)   # disable logs

        # connect to airbnb_test db and create tables
        database.connect()
        database.create_tables([State, City], safe=True)

        # create state record for route
        state_record = State(name='namestring')
        state_record.save()

    def tearDown(self):
        """
        Remove city table from airbnb_test database upon completion of test
        case.
        """
        # drop tables from database
        City.drop_table()
        State.drop_table()

    def createCityViaPeewee(self):
        """
        Create a city record using the API's database/Peewee models.

        createCityViaPeewee returns the Peewee object for the record. This
        method will not work if the database models are not written correctly.
        """
        record = City(name='namestring', state=1)
        record.save()
        return record

    def test_create(self):
        """
        Test proper creation (or non-creation) of city records upon POST
        requests to API.
        """
        # test creation of city with all parameters provided in POST request

        POST_request1 = self.app.post('/states/1/cities', data=dict(
            name='namestring'
        ))

        now = datetime.now().strftime('%d/%m/%Y %H:%M')

        self.assertEqual(City.get(City.id == 1).name, 'namestring')
        self.assertEqual(City.get(City.id == 1).state.id, 1)
        self.assertEqual(City.get(City.id == 1).created_at.strftime('%d/%m/%Y %H:%M'), now)
        self.assertEqual(City.get(City.id == 1).updated_at.strftime('%d/%m/%Y %H:%M'), now)

        # test creation of city in all cases of a parameter missing in POST request
        POST_request2 = self.app.post('/states/1/cities', data=dict())
        self.assertEqual(POST_request2.status[:3], '400')

        # test that city ID for sole record in database is correct
        self.assertEqual(City.select().get().id, 1)

        # test that a post request with a duplicate name value is rejected
        POST_request3 = self.app.post('/states/1/cities', data=dict(
            name='namestring'
        ))

        self.assertEqual(POST_request3.status[:3], '409')
        self.assertEqual(json.loads(POST_request3.data), {'code': 10002, 'msg': 'City already exists in this state'})

    def test_list(self):
        """
        Test proper representation of all city records upon GET requests to
        API.
        """
        GET_request1 = self.app.get('/states/1/cities')
        self.assertEqual(len(json.loads(GET_request1.data)), 0)

        POST_request1 = self.app.post('/states/1/cities', data=dict(
            name='namestring'
        ))

        GET_request2 = self.app.get('/states/1/cities')
        self.assertEqual(len(json.loads(GET_request2.data)), 1)

    def test_get(self):
        """
        Test proper representation of a city record upon GET requests via city
        ID to API
        """
        # set-up for tests
        # ----------------------------------------------------------------------
        # create city record in city table; should have ID 1
        city_record = self.createCityViaPeewee()

        # test for handling of GET request for user record by user id which
        # exists
        # ----------------------------------------------------------------------
        # make GET request for record in table
        GET_request1 = self.app.get('/states/1/cities/1')
        GET_data = json.loads(GET_request1.data)

        # test that status of response is 200
        self.assertEqual(GET_request1.status[:3], '200')

        # test that values of response correctly reflect record in database
        self.assertEqual(city_record.id, GET_data['id'])
        self.assertEqual(city_record.created_at.strftime('%d/%m/%Y %H:%M'), GET_data['created_at'][:-3])
        self.assertEqual(city_record.updated_at.strftime('%d/%m/%Y %H:%M'), GET_data['updated_at'][:-3])
        self.assertEqual(City.get(City.id == 1).name, GET_data['name'])
        self.assertEqual(City.get(City.id == 1).state.id, GET_data['state_id'])

        # test for handling of GET request for city record by city id which
        # does not exist
        # ----------------------------------------------------------------------
        GET_request2 = self.app.get('/states/1/cities/1000')
        self.assertEqual(GET_request2.status[:3], '404')

    def test_delete(self):
        """
        Test deletion of city records upon DELETE requests to API.
        """
        # test response of DELETE request for city by city id
        POST_request1 = self.app.post('/states/1/cities', data=dict(
            name='namestring'
        ))

        GET_request1 = self.app.get('/states/1/cities')

        DELETE_request1 = self.app.delete('/states/1/cities/1')

        GET_request2 = self.app.get('/states/1/cities')

        num_records_b4 = len(json.loads(GET_request1.data))
        num_records_after = len(json.loads(GET_request2.data))

        self.assertEqual(DELETE_request1.status[:3], '200')
        self.assertEqual(num_records_after, num_records_b4 - 1)

        # test response of DELETE request for city by city id which does not exist
        DELETE_request2 = self.app.delete('/states/1/cities/1000')
        self.assertEqual(DELETE_request2.status[:3], '404')
