import json
import logging
import unittest
from datetime import datetime

from peewee import Model

from app import app
from app.views import state
from app.models.state import State
from app.models.base import database




class stateTestCase(unittest.TestCase):
    def setUp(self):
        """
        Overload def setUp(self): to create a test client of airbnb app, and
        create state table in airbnb_test database.
        """
        self.app = app.test_client()        # set up test client
        self.app.testing = True             # set testing to True
        logging.disable(logging.CRITICAL)   # disable logs

        database.connect()                          # connect to airbnb_test db
        database.create_tables([State], safe=True)  # create state table

    def tearDown(self):
        """
        Remove state table from airbnb_test database upon completion of test
        case.
        """
        State.drop_table()  # drop state table from database

    def createStateViaPeewee(self):
        """
        Create a state record using the API's database/Peewee models.

        createStateViaPeewee returns the Peewee object for the record. This
        method will not work if the database models are not written correctly.
        """
        record = State(name='namestring')
        record.save()
        return record

    def test_create(self):
        """
        Test proper creation (or non-creation) of state records upon POST
        requests to API.
        """
        # test creation of state with all parameters provided in POST request

        State.drop_table()
        database.create_tables([State], safe=True)

        POST_request1 = self.app.post('/states', data=dict(
            name='namestring'
        ))

        self.assertEqual(POST_request1.status[:3], '200')

        now = datetime.now().strftime('%d/%m/%Y %H:%M')

        self.assertEqual(State.get(State.id == 1).name, 'namestring')
        self.assertEqual(State.get(State.id == 1).created_at.strftime('%d/%m/%Y %H:%M'), now)
        self.assertEqual(State.get(State.id == 1).updated_at.strftime('%d/%m/%Y %H:%M'), now)

        # test creation of state in all cases of a parameter missing in POST request
        POST_request2 = self.app.post('/states', data=dict())
        self.assertEqual(POST_request2.status[:3], '400')

        # test that state ID for sole record in database is correct
        self.assertEqual(State.select().get().id, 1)

        # test that a post request with a duplicate name value is rejected
        POST_request3 = self.app.post('/states', data=dict(
            name='namestring'
        ))

        self.assertEqual(POST_request3.status[:3], '409')
        self.assertEqual(json.loads(POST_request3.data), {'code': 10001, 'msg': 'State already exists'})

    def test_list(self):
        """
        Test proper representation of all state records upon GET requests to
        API.
        """
        GET_request1 = self.app.get('/states')
        self.assertEqual(len(json.loads(GET_request1.data)), 0)

        POST_request1 = self.app.post('/states', data=dict(
            name='namestring'
        ))

        GET_request2 = self.app.get('/states')
        self.assertEqual(len(json.loads(GET_request2.data)), 1)

    def test_get(self):
        """
        Test proper representation of a state record upon GET requests
        via amenity ID to API.
        """
        # test response of GET request for state by state id
        state_record = self.createStateViaPeewee()

        GET_request1 = self.app.get('/states/1')
        GET_data = json.loads(GET_request1.data)
        self.assertEqual(GET_request1.status[:3], '200')

        self.assertEqual(state_record.id, GET_data['id'])
        self.assertEqual(state_record.created_at.strftime('%d/%m/%Y %H:%M'), GET_data['created_at'][:-3])
        self.assertEqual(state_record.updated_at.strftime('%d/%m/%Y %H:%M'), GET_data['updated_at'][:-3])
        self.assertEqual(state_record.name, GET_data['name'])

        # test response of GET request for state by state id which does not exist
        GET_request2 = self.app.get('/states/1000')
        self.assertEqual(GET_request2.status[:3], '404')

    def test_delete(self):
        """
        Test deletion of state records upon DELETE requests to API.
        """
        # test response of DELETE request for state by state id
        POST_request1 = self.app.post('/states', data=dict(
            name='namestring'
        ))

        GET_request1 = self.app.get('/states')

        DELETE_request1 = self.app.delete('/states/1')

        GET_request2 = self.app.get('/states')

        num_records_b4 = len(json.loads(GET_request1.data))
        num_records_after = len(json.loads(GET_request2.data))

        self.assertEqual(DELETE_request1.status[:3], '200')
        self.assertEqual(num_records_after, num_records_b4 - 1)

        # test response of DELETE request for state by state id which does not exist
        DELETE_request2 = self.app.delete('/states/1000')
        self.assertEqual(DELETE_request2.status[:3], '404')
