import unittest, logging
import config
import os
import json

from app import app
from app.models.city import City
from app.models.state import State
from app.models.base import *
from peewee import Model
from datetime import datetime

class cityTestCase(unittest.TestCase):
    def setUp(self):
        '''overload def setUp(self): to create a test client of airbnb app, and create City
        in airbnb_test database'''
        self.app = app.test_client()
        #self.app.testing = True
        logging.disable(logging.CRITICAL) # disable logs

        database.connect()
        database.create_tables([City, State], safe=True)
        State(name='namestring')


    def tearDown(self):
        '''remove City from airbnb_test database upon completion of test case'''
        City.drop_table()
        State.drop_table()

    def test_create(self):
        '''test proper creation (or non-creation) of city records upon POST requests to API'''
        # test creation of city with all parameters provided in POST request
        POST_request1 = self.app.post('/states/1/cities', data=dict(
            name='namestring'
        ))

        print POST_request1.status
        print POST_request1.data

        now = datetime.now().strftime('%d/%m/%Y %H:%M')

        self.assertEqual(City.get(City.id == 1).name, 'namestring')
        self.assertEqual(City.get(City.id == 1).state, 1)
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

        self.assertEqual(POST_request6.status[:3], '409')
        self.assertEqual(POST_request6.data, json.dumps({'code': 10002, 'msg': 'City already exists in this state'}))

    def test_list(self):
        '''test proper representation of all city records upon GET requests to API'''
        # delete and recreate City table for test
        City.drop_table()
        database.create_tables([City], safe=True)

        GET_request1 = self.app.get('/states/1/cities')
        self.assertEqual(len(json.loads(GET_request1.data)), 0)

        POST_request1 = self.app.post('/states/1/cities', data=dict(
            name='namestring'
        ))

        GET_request2 = self.app.get('/states/1/cities')
        self.assertEqual(len(json.loads(GET_request2.data)), 1)

    def test_get(self):
        '''test proper representation of a city record upon GET requests via city ID to API'''
        # delete and recreate City table for test
        City.drop_table()
        database.create_tables([City], safe=True)

        # test response of GET request for state by state id
        POST_request1 = self.app.post('/states/1/cities', data=dict(
            name='namestring'
        ))

        GET_request1 = self.app.get('/states/1/cities/1')
        GET_data = json.dumps(GET_request1.data)
        self.assertEqual(GET_request.status[:3], '200')

        self.assertEqual(City.get(City.id == 1).name, GET_data[0]['name'])
        self.assertEqual(City.get(City.id == 1).state, GET_data[0]['state'])
        self.assertEqual(City.get(City.id == 1).created_at.strftime('%d/%m/%Y %H:%M'), now)
        self.assertEqual(City.get(City.id == 1).updated_at.strftime('%d/%m/%Y %H:%M'), now)

        # test response of GET request for city by city id which does not exist
        GET_request2 = self.app.get('/states/1/cities/1000')
        self.assertEqual(GET_request2.status[:3], '404')

    def test_delete(self):
        '''test deletion of city records upon DELETE requests to API'''
        # delete and recreate City table for test
        City.drop_table()
        database.create_tables([City], safe=True)

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
