import unittest, logging
import config
import os
import json

from app import app
from app.views.index import *
from app.views.user import *
from app.models.user import User
from app.models.base import *

from peewee import Model
from datetime import datetime


class userTestCase(unittest.TestCase):
    def setUp(self):
        """
        Overload def setUp(self): to create a test client of airbnb app, and
        create amenity table in airbnb_test database.
        """
        self.app = app.test_client()
        self.app.testing = True
        logging.disable(logging.CRITICAL) # disable logs

        # connect to airbnb_test database and create User table
        database.connect()
        database.create_tables([User], safe=True)

    def tearDown(self):
        """
        Remove amenity table from airbnb_test database upon completion of test
        case.
        """
        User.drop_table()

    def createUserViaPeewee(self):
        """
        Create an amenity record using the API's database/Peewee models.

        createAmenityViaPeewee returns the Peewee object for the record. This
        method will not work if the database models are not written correctly.
        """
        record = User(  email='anystring',
                        password='anystring1',
                        first_name='anystring2',
                        last_name='anystring3'  )
        record.save()
        return record

    def createUserViaAPI(self):
        """
        Create an amenity record through a POST request to the API.

        createAmenityViaAPI returns the Flask response object for the request.
        This method will not work if the POST request handler is not written
        properly.
        """
        POST_request = self.app.post('/users', data=dict(
            email='anystring',
            password='anystring1',
            first_name='anystring2',
            last_name='anystring3'
        ))

        return POST_request

    def subtest_createWithAllParams(self):
        """
        Test proper creation of an amenity record upon POST request to the API
        with all parameters provided.
        """
        POST_request1 = self.createUserViaAPI()
        self.assertEqual(POST_request1.status[:3], '200')

        now = datetime.now().strftime('%d/%m/%Y %H:%M')

        self.assertEqual(User.get(User.id == 1).email, 'anystring')
        self.assertEqual(User.get(User.id == 1).password, 'anystring1')
        self.assertEqual(User.get(User.id == 1).first_name, 'anystring2')
        self.assertEqual(User.get(User.id == 1).last_name, 'anystring3')
        self.assertEqual(User.get(User.id == 1).created_at.strftime('%d/%m/%Y %H:%M'), now)
        self.assertEqual(User.get(User.id == 1).updated_at.strftime('%d/%m/%Y %H:%M'), now)
        self.assertEqual(User.get(User.id == 1).is_admin, False)

    def subtest_createWithoutAllParams(self):
        """
        Test proper non-creation of an amenity in all cases of a parameter
        missing in POST request to the API.
        """
        POST_request2 = self.app.post('/users', data=dict(
            password='anystring1',
            first_name='anystring2',
            last_name='anystring3'
        ))

        POST_request3 = self.app.post('/users', data=dict(
            email='anystring10',
            first_name='anystring2',
            last_name='anystring3'
        ))

        POST_request4 = self.app.post('/users', data=dict(
            email='anystring100',
            password='anystring2',
            last_name='anystring3'
        ))

        POST_request5 = self.app.post('/users', data=dict(
            email='anystring1000',
            password='anystring2',
            first_name='anystring3'
        ))

        for request in [POST_request2, POST_request3, POST_request4, POST_request5]:
            self.assertEqual(request.status[:3], '400')

    def test_create(self):
        """
        Test proper creation (or non-creation) of amenity records upon POST
        requests to API.
        """
        # test creation of user with all parameters provided in POST request
        self.subtest_createWithAllParams()

        # test creation of user in all cases of a parameter missing in POST request
        self.subtest_createWithoutAllParams()

        # test that user ID for sole record in database is correct
        self.assertEqual(User.select().get().id, 1)

        # test that a post request with a duplicate email value is rejected
        POST_request6 = self.app.post('/users', data=dict(
            email='anystring',
            password='anystring1',
            first_name='anystring2',
            last_name='anystring3'
        ))

        self.assertEqual(POST_request6.status[:3], '409')
        self.assertEqual(json.loads(POST_request6.data), {
            'code': 10000, 'msg': 'Email already exists'
            }
        )

    def test_list(self):
        """
        Test proper representation of all amenity records upon GET requests to
        API.
        """
        # delete and recreate User table for test
        User.drop_table()
        database.create_tables([User], safe=True)

        GET_request1 = self.app.get('/users')
        self.assertEqual(len(json.loads(GET_request1.data)), 0)

        self.createUserViaPeewee()

        GET_request2 = self.app.get('/users')
        self.assertEqual(len(json.loads(GET_request2.data)), 1)

    def test_get(self):
        """
        Test proper representation of an amenity record upon GET requests
        via amenity ID to API.
        """
        # set-up for tests
        # ----------------------------------------------------------------------
        # delete and recreate user table for test
        User.drop_table()
        database.create_tables([User], safe=True)

        # create user record in user table; should have ID 1
        user_record = self.createUserViaPeewee()

        # test for handling of GET request for user record by user id which
        # exists
        # ----------------------------------------------------------------------
        # make GET request for record in table
        GET_request1 = self.app.get('/users/1')
        GET_data = json.loads(GET_request1.data)

        # test that status of response is 200
        self.assertEqual(GET_request1.status[:3], '200')

        # test that values of response correctly reflect record in database
        self.assertEqual(user_record.id, GET_data['id'])
        self.assertEqual(user_record.created_at.strftime('%d/%m/%Y %H:%M'), GET_data['created_at'][:-3])
        self.assertEqual(user_record.updated_at.strftime('%d/%m/%Y %H:%M'), GET_data['updated_at'][:-3])
        self.assertEqual(user_record.email, GET_data['email'])
        self.assertEqual(user_record.first_name, GET_data['first_name'])
        self.assertEqual(user_record.last_name, GET_data['last_name'])
        self.assertEqual(user_record.is_admin, GET_data['is_admin'])

        # test for handling of GET request for user record by user id which does
        # not exist
        # ----------------------------------------------------------------------
        GET_request2 = self.app.get('/users/1000')
        self.assertEqual(GET_request2.status[:3], '404')

    def test_delete(self):
        """
        Test deletion of amenity records upon DELETE requests to API.
        """
        # delete and recreate User table for test
        User.drop_table()
        database.create_tables([User], safe=True)

        # test response of DELETE request for user by user id
        self.createUserViaPeewee()

        GET_request1 = self.app.get('/users')

        DELETE_request1 = self.app.delete('/users/1')

        GET_request2 = self.app.get('/users')

        num_records_b4 = len(json.loads(GET_request1.data))
        num_records_after = len(json.loads(GET_request2.data))

        self.assertEqual(DELETE_request1.status[:3], '200')
        self.assertEqual(num_records_after, num_records_b4 - 1)

        # test response of DELETE request for user by user id which does not exist
        DELETE_request2 = self.app.delete('/users/1000')
        self.assertEqual(DELETE_request2.status[:3], '404')

    def test_update(self):
        """
        Test update of user records upon PUT requests to API.
        """
        # delete and recreate User table for test
        User.drop_table()
        database.create_tables([User], safe=True)

        self.createUserViaPeewee()

        PUT_request1 = self.app.put('/users/1', data=dict(
            email='anystring2',
            password='anystring3',
            first_name='anystring4',
            last_name='anystring5'
        ))
        self.assertEqual(PUT_request1.status[:3], '200')

        self.assertEqual(User.get(User.id == 1).email, 'anystring2')
        self.assertEqual(User.get(User.id == 1).password, 'anystring3')
        self.assertEqual(User.get(User.id == 1).first_name, 'anystring4')
        self.assertEqual(User.get(User.id == 1).last_name, 'anystring5')

        # test response of PUT request for user by user id which does not exist
        PUT_request2 = self.app.put('/users/1000')
        self.assertEqual(PUT_request2.status[:3], '404')
