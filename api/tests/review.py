import logging
import json
import unittest
from datetime import datetime

from peewee import Model

from app import app
from app.views import review
from app.models.review import Review
from app.models.user import User
from app.models.base import database

"""
notes:
message and review_id are required parameters to make a review record
stars is an optional parameter to specify for review records

assumptions so far:
There's a file called review.py housing the handlers to review routes.
There's a file called review.py housing the Review model for a review table in the db.
There's table that will house review records in the database.
You can't create any review records unless a user id exists.

user_id: int/foreign key field
message: string
stars: int

parameters for post request should be message and optionally stars.
user_id will be specified by uri/url.

POST to /users/<user_id>/reviews:
creates a review associated with given user

GET to /users/<user_id>/reviews:
returns a list of reviews associated with given user

GET to /users/<user_id>/<review_id>:
returns a hash of the review specified in uri
"""

class reviewTestCase(unittest.TestCase):
    def setUp(self):
        """
        Overload def setUp(self): to create a test client of airbnb app, and
        create review table in airbnb_test database.
        """
        self.app = app.test_client()        # set up test client
        self.app.testing = True             # set testing to True
        logging.disable(logging.CRITICAL)   # disable logs

        database.connect()                          # connect to airbnb_test db
        database.create_tables([User, Review], safe=True)   # create tables

        # create user record for foreign key association
        user_record = User(
            email='anystring',
            password='anystring1',
            first_name='anystring2',
            last_name='anystring3'
        )
        user_record.save()


    def tearDown(self):
        """
        Remove review table from airbnb_test database upon completion of test
.
        """
        Review.drop_table()     # drop review table from database
        User.drop_table()       # drop user table from database

    def createReviewViaPeewee(self):
        """
        Create an review record using the API's database/Peewee models.

        createReviewViaPeewee returns the Peewee object for the record. This
        method will not work if the database models are not written correctly.
        """
        record = Review(
            message='foo-message',
            user_id=1,
            stars=5
        )
        record.save()
        return record

    def createReviewViaAPI(self):
        """
        Create an review record through a POST request to the API.

        createReviewViaAPI returns the Flask response object for the request.
        This method will not work if the POST request handler is not written
        properly.
        """
        POST_request = self.app.post('/users/1/reviews', data=dict(
            message='foo-message',
            # user_id omitted since req. handler should get from uri
            stars=5
        ))

        return POST_request

    def subtest_createWithAllParams(self):
        """
        Test proper creation of an review record upon POST request to the API
        with all parameters provided.
        """
        POST_request = self.app.post('/users/1/reviews', data=dict(
            message='foo-message',
            # user_id omitted since req. handler should get from uri
            stars=5
        ))
        self.assertEqual(POST_request1.status[:3], '200')

        now = datetime.now().strftime('%d/%m/%Y %H:%M')

        self.assertEqual(Review.get(Review.id == 1).message, 'foo-message')
        self.assertEqual(Review.get(Review.id == 1).user.id, 1)
        self.assertEqual(Review.get(Review.id == 1).stars, 5)
        self.assertEqual(Review.get(Review.id == 1).created_at.strftime('%d/%m/%Y %H:%M'), now)
        self.assertEqual(Review.get(Review.id == 1).updated_at.strftime('%d/%m/%Y %H:%M'), now)

    def subtest_createWithoutAllParams(self):
        """
        Test proper non-creation (or creation) of an review in all cases of a
        parameter missing in POST request to the API.
        """
        # test that request missing optional stars param is handled w/ success
        # ----------------------------------------------------------------------
        POST_request2 = self.app.post('/users/1/reviews', data=dict(
            message='foo-message'
        ))
        self.assertEqual(POST_request2.status[:3], '200')

        # test that request missing optional stars param fails
        # ----------------------------------------------------------------------
        POST_request3 = self.app.post('/users/1/reviews', data=dict(
            stars=5
        ))
        self.assertEqual(POST_request3.status[:3], '400')

    def test_create(self):
        """
        Test proper creation (or non-creation) of review records upon POST
        requests to API.
        """
        # test response to POST request to user ID which does not exist
        # ----------------------------------------------------------------------
        xPOST_request = self.app.post('/users/1000/reviews', data=dict(
            message='foo-message',
            # user_id omitted since req. handler should get from uri
            stars=5
        ))
        self.assertEqual(len(json.loads(xPOST_request.data)), 404)

        # test creation of review with all parameters provided in POST request
        # ----------------------------------------------------------------------
        self.subtest_createWithAllParams()

        # test that review ID for sole record in database is correct
        # ----------------------------------------------------------------------
        self.assertEqual(Review.select().get().id, 1)

        # test creatxn of review in all cases of parameter missing in POST req.
        # ----------------------------------------------------------------------
        self.subtest_createWithoutAllParams()

    def test_list(self):
        """
        Test proper representation of all review records upon GET requests to
        API.
        """
        # test response to GET request by user ID which does not exist
        # ----------------------------------------------------------------------
        GET_request1 = self.app.get('users/1000/reviews')
        self.assertEqual(len(json.loads(GET_request1.data)), 404)

        # test response to GET request by user ID which exists
        # ----------------------------------------------------------------------
        GET_request1 = self.app.get('users/1/reviews')
        self.assertEqual(len(json.loads(GET_request1.data)), 0)

        self.createReviewViaPeewee()

        GET_request2 = self.app.get('users/1/reviews')
        self.assertEqual(len(json.loads(GET_request2.data)), 1)

    def test_get(self):
        """
        Test proper representation of an review record upon GET requests
        via review ID to API.
        """
        # set-up for tests
        # ----------------------------------------------------------------------
        # create review record in review table; should have ID 1
        review_record = self.createReviewViaPeewee()

        # test handling of GET req. for record by user & review IDs which exist
        # ----------------------------------------------------------------------
        # make GET request for record in table
        GET_request1 = self.app.get('/user/1/1')
        GET_data = json.loads(GET_request1.data)

        # test that status of response is 200
        self.assertEqual(GET_request1.status[:3], '200')

        # test that values of response correctly reflect record in database
        self.assertEqual(review_record.id, GET_data['id'])
        self.assertEqual(review_record.created_at.strftime('%d/%m/%Y %H:%M'), GET_data['created_at'][:-3])
        self.assertEqual(review_record.updated_at.strftime('%d/%m/%Y %H:%M'), GET_data['updated_at'][:-3])
        self.assertEqual(review_record.message, GET_data['message'])
        self.assertEqual(review_record.stars, GET_data['stars'])
        self.assertEqual(review_record.user.id, GET_data['user_id'])

        # test handling of GET req. for review record by review ID which exists
        # but user ID which does not
        # ----------------------------------------------------------------------
        GET_request2 = self.app.get('/users/1000/1')
        self.assertEqual(GET_request2.status[:3], '404')

        # test handling of GET req. for review record by user ID which exists
        # but review id which does not
        # ----------------------------------------------------------------------
        GET_request2 = self.app.get('/users/1/1000')
        self.assertEqual(GET_request2.status[:3], '404')

    def test_delete(self):
        """
        Test deletion of review records upon DELETE requests to API.
        """
        # test response to DELETE request for review by review id
        # ----------------------------------------------------------------------
        self.createReviewViaPeewee()

        GET_request1 = self.app.get('users/1/reviews')

        DELETE_request1 = self.app.delete('/users/1/1')

        GET_request2 = self.app.get('users/1/reviews')

        num_records_b4 = len(json.loads(GET_request1.data))
        num_records_after = len(json.loads(GET_request2.data))

        self.assertEqual(DELETE_request1.status[:3], '200')
        self.assertEqual(num_records_after, num_records_b4 - 1)

        # test handling of DELETE req. for review record by review ID which
        # exists but user ID which does not
        # ----------------------------------------------------------------------
        DELETE_request2 = self.app.delete('/users/1000/1')
        self.assertEqual(DELETE_request2.status[:3], '404')

        # test handling of DELETE req. for review record by user ID which
        # exists but review ID which does not
        # ----------------------------------------------------------------------
        DELETE_request2 = self.app.delete('/users/1/1000')
        self.assertEqual(DELETE_request2.status[:3], '404')
