import unittest, logging
import config
import os
import json

from app import app
from app.views.amenity import *
from app.models.amenity import Amenity
from app.models.base import *
from peewee import Model
from datetime import datetime


class amenityTestCase(unittest.TestCase):
    def setUp(self):
        """
        Overload def setUp(self): to create a test client of airbnb app, and
        create amenity table in airbnb_test database.
        """
        self.app = app.test_client()
        self.app.testing = True
        logging.disable(logging.CRITICAL) # disable logs

        # connect to airbnb_test database and create Amenity table
        database.connect()
        database.create_tables([Amenity], safe=True)

    def tearDown(self):
        """
        Remove amenity table from airbnb_test database upon completion of test
        case.
        """
        Amenity.drop_table()

    def createAmenityViaPeewee(self):
        """
        Create an amenity record using the API's database/Peewee models.

        createAmenityViaPeewee returns the Peewee object for the record. This
        method will not work if the database models are not written correctly.
        """
        record = Amenity(name= 'amenity_name')
        record.save()
        return record

    def createAmenityViaAPI(self):
        """
        Create an amenity record through a POST request to the API.

        createAmenityViaAPI returns the Flask response object for the request.
        This method will not work if the POST request handler is not written
        properly.
        """
        POST_request = self.app.post('/amenities', data=dict(
            name= 'amenity_name'
        ))
        return POST_request

    def subtest_createWithAllParams(self):
        """
        Test proper creation of an amenity record upon POST request to the API
        with all parameters provided.
        """
        POST_request1 = self.createAmenityViaAPI()
        self.assertEqual(POST_request1.status[:3], '200')

        now = datetime.now().strftime('%d/%m/%Y %H:%M')

        self.assertEqual(Amenity.get(Amenity.id == 1).name, 'amenity_name')
        self.assertEqual(Amenity.get(Amenity.id == 1).created_at.strftime('%d/%m/%Y %H:%M'), now)
        self.assertEqual(Amenity.get(Amenity.id == 1).updated_at.strftime('%d/%m/%Y %H:%M'), now)

        # test that placebook ID for sole record in database is correct
        self.assertEqual(Amenity.select().get().id, 1)

    def subtest_createWithoutAllParams(self):
        """
        Test proper non-creation of an amenity in all cases of a parameter
        missing in POST request to the API.
        """
        # name missing - request should fail due to no default value
        POST_request2 = self.app.post('/amenities', data=dict())

        self.assertEqual(POST_request2.status[:3], '400')

    def test_create(self):
        """
        Test proper creation (or non-creation) of amenity records upon POST
        requests to API.
        """
        # test creation of amenity with all parameters provided in POST request
        self.subtest_createWithAllParams()

        # test creation of amenity in all cases of a parameter missing in POST request
        self.subtest_createWithoutAllParams()

    def test_list(self):
        """
        Test proper representation of all amenity records upon GET requests to
        API.
        """
        GET_request1 = self.app.get('/amenities')
        self.assertEqual(len(json.loads(GET_request1.data)), 0)

        self.createAmenityViaPeewee()

        GET_request2 = self.app.get('/amenities')
        self.assertEqual(len(json.loads(GET_request2.data)), 1)

        # could also test to make sure records returned only belong to respect-
        # ive place

    def test_get(self):
        """
        Test proper representation of an amenity record upon GET requests
        via amenity ID to API.
        """
        # test response of GET request for placebook by placebook id
        amenity_record = self.createAmenityViaPeewee()

        GET_request1 = self.app.get('/amenities/1')
        GET_data = json.loads(GET_request1.data)
        self.assertEqual(GET_request1.status[:3], '200')

        self.assertEqual(amenity_record.id, GET_data['id'])
        self.assertEqual(amenity_record.created_at.strftime('%d/%m/%Y %H:%M'), GET_data['created_at'][:-3])
        self.assertEqual(amenity_record.updated_at.strftime('%d/%m/%Y %H:%M'), GET_data['updated_at'][:-3])
        self.assertEqual(amenity_record.name, GET_data['name'])

        # test response of GET request for booking by booking id which does not exist
        GET_request2 = self.app.get('/amenities/1000')
        self.assertEqual(GET_request2.status[:3], '404')

    def test_delete(self):
        """
        Test deletion of amenity records upon DELETE requests to API.
        """
        # test response of DELETE request for amenity by amenity id
        self.createAmenityViaPeewee()

        GET_request1 = self.app.get('/amenities')

        DELETE_request1 = self.app.delete('/amenities')

        GET_request2 = self.app.get('/amenities')

        num_records_b4 = len(json.loads(GET_request1.data))
        num_records_after = len(json.loads(GET_request2.data))

        self.assertEqual(DELETE_request1.status[:3], '200')
        self.assertEqual(num_records_after, num_records_b4 - 1)

        # test response of DELETE request for amenity by amenity id which does not exist
        DELETE_request2 = self.app.delete('/amenities/1000')
        self.assertEqual(DELETE_request2.status[:3], '404')
