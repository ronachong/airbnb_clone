import logging
import json
import unittest
from datetime import datetime

from peewee import Model

from app import app
from app.views import review
from app.models.review import Review
from app.models.user import User
from app.models.city import City
from app.models.state import State
from app.models.Place import Place
from app.models.base import database


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
        database.create_tables(                     # create tables
            [User, State, City, Place, Review],
            safe=True
        )

        # create user record for foreign key association
        user_record = User(
            email='anystring',
            password='anystring1',
            first_name='anystring2',
            last_name='anystring3'
        )
        user_record.save()

        # create place records (and dependencies) for foreign key association
        state_record = State(name='foo-state')
        state_record.save()
        city_record = City(name='foo-city', state=1)
        city_record.save()
        place_record = Place(
            owner_id=1,
            city_id=1,
            name="foo",
            description="foo description",
            number_rooms=1,
            number_bathrooms=1,
            max_guest=1,
            price_by_night=1,
            latitude=20.0,
            longitude=22.0
        )
        place_record.save()

    def tearDown(self):
        """Remove tables from airbnb_test database upon completion of test."""
        Review.drop_table()
        Place.drop_table()
        City.drop_table()
        State.drop_table
        User.drop_table()

    def createUserReviewViaPeewee(self):
        """Create a user review record using the API's database/Peewee models.

        createUserReviewViaPeewee returns the Peewee object for the record.
        This method will not work if the database models are not written
        correctly.
        """
        record = ReviewUser(
            message='foo-message',
            user_id=1,
            stars=5
        )
        record.save()
        return record

    def createPlaceReviewViaPeewee(self):
        """Create a user review record using the API's database/Peewee models.

        createPlaceReviewViaPeewee returns the Peewee object for the record.
        This method will not work if the database models are not written
        correctly.
        """
        record = ReviewPlace(
            message='foo-message',
            place_id=1,
            stars=5
        )
        record.save()
        return record

    def createReviewViaAPI_uroute(self):
        """Create a user review record through a POST request to the API.

        createReviewViaAPI_uroute returns the Flask response object for the
        request.
        This method will not work if the POST request handler is not written
        properly.
        """
        POST_request = self.app.post('/users/1/reviews', data=dict(
            message='foo-message',
            # user_id omitted since req. handler should get from uri
            stars=5
        ))

        return POST_request

    def createReviewViaAPI_proute(self):
        """Create a place review record through a POST request to the API.

        createReviewViaAPI_proute returns the Flask response object for the
        request. This method will not work if the POST request handler is not
        written properly.
        """
        POST_request = self.app.post('/places/1/reviews', data=dict(
            message='foo-message',
            # place_id omitted since req. handler should get from uri
            stars=5
        ))

        return POST_request

"""Tests for user reviews."""

    def subtest_createWithAllParams_uroute(self):
        """
        Test proper creation of a user review record upon POST request to the
        API with all parameters provided.
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

    def subtest_createWithoutAllParams_uroute(self):
        """
        Test proper non-creation (or creation) of a user review in all cases of
        a parameter missing in POST request to the API.
        """
        # test that request missing optional stars param is handled w/ success
        # ----------------------------------------------------------------------
        POST_request2 = self.app.post('/users/1/reviews', data=dict(
            message='foo-message'
        ))
        self.assertEqual(POST_request2.status[:3], '200')

        # test that request missing mandatory message param fails
        # ----------------------------------------------------------------------
        POST_request3 = self.app.post('/users/1/reviews', data=dict(
            stars=5
        ))
        self.assertEqual(POST_request3.status[:3], '400')

    def test_create_uroute(self):
        """
        Test proper creation (or non-creation) of user review records upon POST
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
        self.subtest_createWithAllParams_uroute()

        # test that review ID for sole record in database is correct
        # ----------------------------------------------------------------------
        self.assertEqual(Review.select().get().id, 1)

        # test creatxn of review in all cases of parameter missing in POST req.
        # ----------------------------------------------------------------------
        self.subtest_createWithoutAllParams_uroute()

    def test_list_uroute(self):
        """
        Test proper representation of user review records upon GET requests
        to API.
        """
        # test response to GET request by user ID which does not exist
        # ----------------------------------------------------------------------
        GET_request1 = self.app.get('users/1000/reviews')
        self.assertEqual(len(json.loads(GET_request1.data)), 404)

        # test response to GET request by user ID which exists
        # ----------------------------------------------------------------------
        GET_request2 = self.app.get('users/1/reviews')
        self.assertEqual(len(json.loads(GET_request2.data)), 0)

        self.createUserReviewViaPeewee()

        GET_request3 = self.app.get('users/1/reviews')
        self.assertEqual(len(json.loads(GET_request3.data)), 1)

    def test_get_uroute(self):
        """
        Test proper representation of a user review record upon GET requests
        via review ID to API.
        """
        # set-up for tests
        # ----------------------------------------------------------------------
        # create review record in review table; should have ID 1
        review_record = self.createUserReviewViaPeewee()

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

    def test_delete_uroute(self):
        """
        Test deletion of user review records upon DELETE requests to API.
        """
        # test response to DELETE request for review by review id
        # ----------------------------------------------------------------------
        self.createUserReviewViaPeewee()

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


"""Tests for place reviews."""

    def subtest_createWithAllParams_proute(self):
        """
        Test proper creation of a place review record upon POST request to the
        API with all parameters provided.
        """
        POST_request = self.app.post('/places/1/reviews', data=dict(
            message='foo-message',
            # place_id omitted since req. handler should get from uri
            stars=5
        ))
        self.assertEqual(POST_request1.status[:3], '200')

        now = datetime.now().strftime('%d/%m/%Y %H:%M')

        self.assertEqual(Review.get(Review.id == 1).message, 'foo-message')
        self.assertEqual(Review.get(Review.id == 1).place.id, 1)
        self.assertEqual(Review.get(Review.id == 1).stars, 5)
        self.assertEqual(Review.get(Review.id == 1).created_at.strftime('%d/%m/%Y %H:%M'), now)
        self.assertEqual(Review.get(Review.id == 1).updated_at.strftime('%d/%m/%Y %H:%M'), now)

    def subtest_createWithoutAllParams_proute(self):
        """
        Test proper non-creation (or creation) of a place review in all cases
        of a parameter missing in POST request to the API.
        """
        # test that request missing optional stars param is handled w/ success
        # ----------------------------------------------------------------------
        POST_request2 = self.app.post('/places/1/reviews', data=dict(
            message='foo-message'
        ))
        self.assertEqual(POST_request2.status[:3], '200')

        # test that request missing mandatory message param fails
        # ----------------------------------------------------------------------
        POST_request3 = self.app.post('/place/1/reviews', data=dict(
            stars=5
        ))
        self.assertEqual(POST_request3.status[:3], '400')

    def test_create_proute(self):
        """
        Test proper creation (or non-creation) of place review records upon
        POST requests to API.
        """
        # test response to POST request to place ID which does not exist
        # ----------------------------------------------------------------------
        xPOST_request = self.app.post('/place/1000/reviews', data=dict(
            message='foo-message',
            # place_id omitted since req. handler should get from uri
            stars=5
        ))
        self.assertEqual(len(json.loads(xPOST_request.data)), 404)

        # test creation of review with all parameters provided in POST request
        # ----------------------------------------------------------------------
        self.subtest_createWithAllParams_uroute()

        # test that review ID for sole record in database is correct
        # ----------------------------------------------------------------------
        self.assertEqual(Review.select().get().id, 1)

        # test creatxn of review in all cases of parameter missing in POST req.
        # ----------------------------------------------------------------------
        self.subtest_createWithoutAllParams_uroute()

    def test_list_proute(self):
        """
        Test proper representation of all place review records upon GET
        requests to API.
        """
        # test response to GET request by place ID which does not exist
        # ----------------------------------------------------------------------
        GET_request1 = self.app.get('places/1000/reviews')
        self.assertEqual(len(json.loads(GET_request1.data)), 404)

        # test response to GET request by place ID which exists
        # ----------------------------------------------------------------------
        GET_request2 = self.app.get('places/1/reviews')
        self.assertEqual(len(json.loads(GET_request2.data)), 0)

        self.createPlaceReviewViaPeewee()

        GET_request3 = self.app.get('places/1/reviews')
        self.assertEqual(len(json.loads(GET_request3.data)), 1)

    def test_get_proute(self):
        """
        Test proper representation of a place review record upon GET requests
        via review ID to API.
        """
        # set-up for tests
        # ----------------------------------------------------------------------
        # create review record in review table; should have ID 1
        review_record = self.createPlaceReviewViaPeewee()

        # test handling of GET req. for record by place & review IDs which exist
        # ----------------------------------------------------------------------
        # make GET request for record in table
        GET_request1 = self.app.get('/place/1/1')
        GET_data = json.loads(GET_request1.data)

        # test that status of response is 200
        self.assertEqual(GET_request1.status[:3], '200')

        # test that values of response correctly reflect record in database
        self.assertEqual(review_record.id, GET_data['id'])
        self.assertEqual(review_record.created_at.strftime('%d/%m/%Y %H:%M'), GET_data['created_at'][:-3])
        self.assertEqual(review_record.updated_at.strftime('%d/%m/%Y %H:%M'), GET_data['updated_at'][:-3])
        self.assertEqual(review_record.message, GET_data['message'])
        self.assertEqual(review_record.stars, GET_data['stars'])
        self.assertEqual(review_record.place.id, GET_data['place_id'])

        # test handling of GET req. for review record by review ID which exists
        # but place ID which does not
        # ----------------------------------------------------------------------
        GET_request2 = self.app.get('/places/1000/1')
        self.assertEqual(GET_request2.status[:3], '404')

        # test handling of GET req. for review record by place ID which exists
        # but review id which does not
        # ----------------------------------------------------------------------
        GET_request2 = self.app.get('/places/1/1000')
        self.assertEqual(GET_request2.status[:3], '404')

    def test_delete_proute(self):
        """
        Test deletion of place review records upon DELETE requests to API.
        """
        # test response to DELETE request for review by review id
        # ----------------------------------------------------------------------
        self.createPlaceReviewViaPeewee()

        GET_request1 = self.app.get('places/1/reviews')
        DELETE_request1 = self.app.delete('/places/1/1')
        GET_request2 = self.app.get('places/1/reviews')

        num_records_b4 = len(json.loads(GET_request1.data))
        num_records_after = len(json.loads(GET_request2.data))

        self.assertEqual(DELETE_request1.status[:3], '200')
        self.assertEqual(num_records_after, num_records_b4 - 1)

        # test handling of DELETE req. for review record by review ID which
        # exists but place ID which does not
        # ----------------------------------------------------------------------
        DELETE_request2 = self.app.delete('/places/1000/1')
        self.assertEqual(DELETE_request2.status[:3], '404')

        # test handling of DELETE req. for review record by place ID which
        # exists but review ID which does not
        # ----------------------------------------------------------------------
        DELETE_request2 = self.app.delete('/places/1/1000')
        self.assertEqual(DELETE_request2.status[:3], '404')
