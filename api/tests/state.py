import unittest, logging
import config
import os
import json

from app import app
from app.views import *
from app.models.state import State
from app.models.base import *
from peewee import Model
from datetime import datetime

class stateTestCase(unittest.TestCase):
    def setUp(self):
        '''overload def setUp(self): to create a test client of airbnb app, and create State
        in airbnb_test database'''
        self.app = app.test_client()
        #self.app.testing = True
        logging.disable(logging.CRITICAL) # disable logs

        database.connect()
        database.create_tables([State], safe=True)

    def tearDown(self):
        '''remove State from airbnb_test database upon completion of test case'''
        State.drop_table()

    def test_create(self):
        '''test proper creation (or non-creation) of state records upon POST requests to API'''
        # test creation of state with all parameters provided in POST request

        State.drop_table()
        database.create_tables([State], safe=True)

        POST_request1 = self.app.post('/states', data=dict(
            name='namestring'
        ))

        self.assertEqual(POST_request1.status[:3], '200')

        now = datetime.now().strftime('%d/%m/%Y %H:%M')

        self.assertEqual(State.get(State.id == 1).name, 'namestring')
        self.assertEqual(State.get(State.id == 1).created_at[:-3], now)
        self.assertEqual(State.get(State.id == 1).updated_at[:-3], now)

        # test creation of state in all cases of a parameter missing in POST request
        POST_request2 = self.app.post('/states', data=dict())
        self.assertEqual(POST_request2.status[:3], '400')

        # test that state ID for sole record in database is correct
        self.assertEqual(State.select().get().id, 1)

        # test that a post request with a duplicate name value is rejected
        POST_request3 = self.app.post('/states', data=dict(
            name='namestring'
        ))

        self.assertEqual(POST_request6.status[:3], '409')
        self.assertEqual(POST_request6.data, json.dumps({'code': 10001, 'msg': 'State already exists'}))

    def test_list(self):
        '''test proper representation of all state records upon GET requests to API'''
        # delete and recreate State table for test
        State.drop_table()
        database.create_tables([State], safe=True)

        GET_request1 = self.app.get('/states')
        self.assertEqual(len(json.loads(GET_request1.data)), 0)

        POST_request1 = self.app.post('/states', data=dict(
            name='namestring'
        ))

        GET_request2 = self.app.get('/states')
        self.assertEqual(len(json.loads(GET_request2.data)), 1)

    def test_get(self):
        '''test proper representation of a state record upon GET requests via state ID to API'''
        # delete and recreate State table for test
        State.drop_table()
        database.create_tables([State], safe=True)

        # test response of GET request for state by state id
        POST_request1 = self.app.post('/states', data=dict(
            name='namestring'
        ))

        GET_request1 = self.app.get('/states/1')
        GET_data = json.dumps(GET_request1.data)
        self.assertEqual(GET_request1.status[:3], '200')

        self.assertEqual(State.get(State.id == 1).name, GET_data[0]['name'])
        self.assertEqual(State.get(State.id == 1).created_at[:-3], now)
        self.assertEqual(State.get(State.id == 1).updated_at[:-3], now)

        # test response of GET request for state by state id which does not exist
        GET_request2 = self.app.get('/states/1000')
        self.assertEqual(GET_request2.status[:3], '404')

    def test_delete(self):
        '''test deletion of state records upon DELETE requests to API'''
        # delete and recreate State table for test
        State.drop_table()
        database.create_tables([State], safe=True)

        # test response of DELETE request for state by state id
        POST_request1 = self.app.post('/states', data=dict(
            name='namestring'
        ))

        GET_request1 = self.app.get('/state')

        DELETE_request1 = self.app.delete('/states/1')

        GET_request2 = self.app.get('/state')

        num_records_b4 = len(json.loads(GET_request1.data))
        num_records_after = len(json.loads(GET_request2.data))

        self.assertEqual(DELETE_request1.status[:3], '200')
        self.assertEqual(num_records_after, num_records_b4 - 1)

        # test response of DELETE request for state by state id which does not exist
        DELETE_request2 = self.app.delete('/states/1000')
        self.assertEqual(DELETE_request2.status[:3], '404')

    def test_update(self):
        '''test update of state records upon PUT requests to API'''
        # delete and recreate State table for test
        State.drop_table()
        database.create_tables([State], safe=True)

        POST_request1 = self.app.post('/states', data=dict(
            name='namestring'
        ))

        PUT_request1 = self.app.put('/states/1', data=dict(
            name='namestring2'
        ))

        self.assertEqual(PUT_request1.status[:3], '200')

        self.assertEqual(State.get(State.id == 1).name, 'namestring2')

        # test response of PUT request for state by state id which does not exist
        PUT_request2 = self.app.put('/states/1000')
        self.assertEqual(PUT_request2.status[:3], '404')
