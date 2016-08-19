import logging
import json
import unittest
from datetime import datetime

from peewee import Model

from app import app
from app.views import review
from app.models.review import Review
from app.models.review_user import ReviewUser
from app.models.review_place import ReviewPlace
from app.models.user import User
from app.models.city import City
from app.models.state import State
from app.models.place import Place
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
            [User, State, City, Place, Review, ReviewUser, ReviewPlace],
            safe=True
        )

        # create user record for routes
        user_record = User(
            email='anystring',
            password='anystring1',
            first_name='anystring2',
            last_name='anystring3'
        )
        user_record.save()

        user_record2 = User(
            email='anystring-2',
            password='anystring1',
            first_name='anystring2',
            last_name='anystring3'
        )
        user_record2.save()

        # create place records (and dependencies) for routes
        state_record = State(name='foo-statee')
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
        ReviewUser.drop_table()
        ReviewPlace.drop_table()
        Review.drop_table()
        Place.drop_table()
        City.drop_table()
        State.drop_table()
        User.drop_table()

    def createReviewViaPeewee(self):
        record = Review(
            message='foo-message',
            user=2,
            stars=5
        )
        record.save()
        return record

    def createUserReviewViaPeewee(self):
        """Create a review record linked to a review user record using the
        API's database/Peewee models.

        createUserReviewViaPeewee returns the Peewee object for the review user
        record. This method will not work if the database models are not
        written correctly.
        """
        # create record in review table
        review = self.createReviewViaPeewee()

        # create record in review user table
        u_review = ReviewUser(
            user=1,
            review=review.id
        )
        u_review.save()

        return u_review

    def createPlaceReviewViaPeewee(self):
        """Create a review record linked to a review place record using the
        API's database/Peewee models.

        createPlaceReviewViaPeewee returns the Peewee object for the review
        place record. This method will not work if the database models are not
        written correctly.
        """
        # create record in review table
        review = self.createReviewViaPeewee()

        # create record in review place table
        p_review = ReviewPlace(
            place=1,
            review=review.id
        )
        p_review.save()

        return p_review

    def createReviewViaAPI_uroute(self):
        """Create a user review record through a POST request to the API.

        createReviewViaAPI_uroute returns the Flask response object for the
        request.  This method will not work if the POST request handler is not
        written properly.
        """
        POST_request = self.app.post('/users/1/reviews', data=dict(
            message='foo-message',
            user_id=2,
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
            user_id=2,
            stars=5
        ))

        return POST_request

        """Tests for user reviews."""

    # def subtest_createWithAllParams_uroute(self):
    #     """
    #     Test proper creation of user review records upon POST request to the
    #     API with all parameters provided.
    #     """
    #
    #     # create records with POST; check for success
    #     # ----------------------------------------------------------------------
    #     POST_request = self.app.post('/users/1/reviews', data=dict(
    #         message='foo-message',
    #         user_id=2,
    #         stars=5
    #     ))
    #     self.assertEqual(POST_request.status[:3], '200')
    #
    #     # validate values stored in db
    #     # ----------------------------------------------------------------------
    #     # for review record
    #     now = datetime.now().strftime('%d/%m/%Y %H:%M')
    #     record = Review.get(Review.id == 1)
    #
    #     self.assertEqual(record.message, 'foo-message')
    #     self.assertEqual(record.user.id, 2)
    #     self.assertEqual(record.stars, 5)
    #     self.assertEqual(record.created_at.strftime('%d/%m/%Y %H:%M'), now)
    #     self.assertEqual(record.updated_at.strftime('%d/%m/%Y %H:%M'), now)
    #
    #     # for review user record
    #     now = datetime.now().strftime('%d/%m/%Y %H:%M')
    #     record = ReviewUser.get(ReviewUser.review == 1)
    #
    #     self.assertEqual(record.user.id, 1)
    #
    # def subtest_createWithoutAllParams_uroute(self):
    #     """
    #     Test proper non-creation (or creation) of a user review in all cases of
    #     a parameter missing in POST request to the API.
    #     """
    #     # test that request missing optional stars param is handled w/ success
    #     # ----------------------------------------------------------------------
    #     POST_request2 = self.app.post('/users/1/reviews', data=dict(
    #         message='foo-message',
    #         user_id=2
    #     ))
    #     self.assertEqual(POST_request2.status[:3], '200')
    #
    #     # test that request missing mandatory message param fails
    #     # ----------------------------------------------------------------------
    #     POST_request3 = self.app.post('/users/1/reviews', data=dict(
    #         stars=5,
    #         user_id=2
    #     ))
    #     self.assertEqual(POST_request3.status[:3], '400')
    #
    #     # test that request missing mandatory user_id param fails
    #     # ----------------------------------------------------------------------
    #     POST_request3 = self.app.post('/users/1/reviews', data=dict(
    #         stars=5,
    #         message='foo-message'
    #     ))
    #     self.assertEqual(POST_request3.status[:3], '400')
    #
    # def test_create_uroute(self):
    #     """
    #     Test proper creation (or non-creation) of user review records upon POST
    #     requests to API.
    #     """
    #     # test response to POST request to user ID which does not exist
    #     # ----------------------------------------------------------------------
    #     xPOST_request = self.app.post('/users/1000/reviews', data=dict(
    #         message='foo-message',
    #         user_id=2,
    #         stars=5
    #     ))
    #
    #     self.assertEqual(xPOST_request.status[:3], '404')
    #
    #     # test creation of review with all parameters provided in POST request
    #     # ----------------------------------------------------------------------
    #     self.subtest_createWithAllParams_uroute()
    #
    #     # test that review ID for sole record in database is correct
    #     # ----------------------------------------------------------------------
    #     self.assertEqual(Review.select().get().id, 1)
    #
    #     # test creatxn of review in all cases of parameter missing in POST req.
    #     # ----------------------------------------------------------------------
    #     self.subtest_createWithoutAllParams_uroute()
    #
    # def test_list_uroute(self):
    #     """
    #     Test proper representation of user review records upon GET requests
    #     to API.
    #     """
    #     # test response to GET request by user ID which does not exist
    #     # ----------------------------------------------------------------------
    #     GET_request1 = self.app.get('users/1000/reviews')
    #     self.assertEqual(GET_request1.status[:3], '404')
    #
    #     # test response to GET request by user ID which exists
    #     # ----------------------------------------------------------------------
    #     GET_request2 = self.app.get('users/1/reviews')
    #     self.assertEqual(len(json.loads(GET_request2.data)), 0)
    #
    #     self.createUserReviewViaPeewee()
    #
    #     GET_request3 = self.app.get('users/1/reviews')
    #     self.assertEqual(len(json.loads(GET_request3.data)), 1)
    #
    # def test_get_uroute(self):
    #     """
    #     Test proper representation of a user review record upon GET requests
    #     via review ID to API.
    #     """
    #     # set-up for tests
    #     # ----------------------------------------------------------------------
    #     # create user review records in review table; should have ID's 1
    #     ur_record = self.createUserReviewViaPeewee()
    #     r_record = ur_record.review
    #
    #     # test handling of GET req. for record by user & review IDs which exist
    #     # ----------------------------------------------------------------------
    #     # make GET request for record in table
    #     GET_request1 = self.app.get('/users/1/reviews/1')
    #     GET_data = json.loads(GET_request1.data)
    #
    #     # test that status of response is 200
    #     self.assertEqual(GET_request1.status[:3], '200')
    #
    #     # test that values of response correctly reflect record in database
    #     self.assertEqual(r_record.id, GET_data['id'])
    #     self.assertEqual(r_record.created_at.strftime('%d/%m/%Y %H:%M'), GET_data['created_at'][:-3])
    #     self.assertEqual(r_record.updated_at.strftime('%d/%m/%Y %H:%M'), GET_data['updated_at'][:-3])
    #     self.assertEqual(r_record.message, GET_data['message'])
    #     self.assertEqual(r_record.stars, GET_data['stars'])
    #     self.assertEqual(r_record.user.id, GET_data['from_user_id'])
    #     self.assertEqual(ur_record.user.id, GET_data['to_user_id'])
    #     self.assertEqual(None, GET_data['to_place_id'])
    #
    #     # test handling of GET req. for review record by review ID which exists
    #     # but user ID which does not
    #     # ----------------------------------------------------------------------
    #     GET_request2 = self.app.get('/users/1000/reviews/1')
    #     self.assertEqual(GET_request2.status[:3], '404')
    #
    #     # test handling of GET req. for review record by user ID which exists
    #     # but review id which does not
    #     # ----------------------------------------------------------------------
    #     GET_request2 = self.app.get('/users/1/reviews/1000')
    #     self.assertEqual(GET_request2.status[:3], '404')
    #
    # def test_delete_uroute(self):
    #     """
    #     Test deletion of user review records upon DELETE requests to API.
    #     """
    #     # test response to DELETE request for review by review id
    #     # ----------------------------------------------------------------------
    #     self.createUserReviewViaPeewee()
    #
    #     GET_request1 = self.app.get('users/1/reviews')
    #     DELETE_request1 = self.app.delete('/users/1/reviews/1')
    #     GET_request2 = self.app.get('users/1/reviews')
    #
    #     num_records_b4 = len(json.loads(GET_request1.data))
    #     num_records_after = len(json.loads(GET_request2.data))
    #
    #     self.assertEqual(DELETE_request1.status[:3], '200')
    #     self.assertEqual(num_records_after, num_records_b4 - 1)
    #
    #     # test handling of DELETE req. for review record by review ID which
    #     # exists but user ID which does not
    #     # ----------------------------------------------------------------------
    #     DELETE_request2 = self.app.delete('/users/1000/reviews/1')
    #     self.assertEqual(DELETE_request2.status[:3], '404')
    #
    #     # test handling of DELETE req. for review record by user ID which
    #     # exists but review ID which does not
    #     # ----------------------------------------------------------------------
    #     DELETE_request2 = self.app.delete('/users/1/reviews/1000')
    #     self.assertEqual(DELETE_request2.status[:3], '404')


        """Tests for place reviews."""

    def subtest_createWithAllParams_proute(self):
        """
        Test proper creation of a place review record upon POST request to the
        API with all parameters provided.
        """
        # create records with POST; check for success
        # ----------------------------------------------------------------------
        POST_request = self.app.post('/places/1/reviews', data=dict(
            message='foo-message',
            user_id=2,
            stars=5
        ))
        self.assertEqual(POST_request.status[:3], '200')

        # validate values stored in db
        # ----------------------------------------------------------------------
        # for review record
        now = datetime.now().strftime('%d/%m/%Y %H:%M')
        record = Review.get(Review.id == 1)

        self.assertEqual(record.message, 'foo-message')
        self.assertEqual(record.user.id, 2)
        self.assertEqual(record.stars, 5)
        self.assertEqual(record.created_at.strftime('%d/%m/%Y %H:%M'), now)
        self.assertEqual(record.updated_at.strftime('%d/%m/%Y %H:%M'), now)

        # for review place record
        now = datetime.now().strftime('%d/%m/%Y %H:%M')
        record = ReviewPlace.get(ReviewPlace.review == 1)

        self.assertEqual(record.place.id, 1)

    def subtest_createWithoutAllParams_proute(self):
        """
        Test proper non-creation (or creation) of a place review in all cases
        of a parameter missing in POST request to the API.
        """
        # test that request missing optional stars param is handled w/ success
        # ----------------------------------------------------------------------
        POST_request2 = self.app.post('/places/1/reviews', data=dict(
            message='foo-message',
            user_id=2
        ))
        self.assertEqual(POST_request2.status[:3], '200')

        # test that request missing mandatory message param fails
        # ----------------------------------------------------------------------
        POST_request3 = self.app.post('/places/1/reviews', data=dict(
            stars=5,
            user_id=2
        ))
        self.assertEqual(POST_request3.status[:3], '400')

        # test that request missing mandatory user_id param fails
        # ----------------------------------------------------------------------
        POST_request4 = self.app.post('/places/1/reviews', data=dict(
            stars=5,
            message='foo-message'
        ))
        self.assertEqual(POST_request4.status[:3], '400')

    def test_create_proute(self):
        """
        Test proper creation (or non-creation) of place review records upon
        POST requests to API.
        """
        # test response to POST request to place ID which does not exist
        # ----------------------------------------------------------------------
        xPOST_request = self.app.post('/place/1000/reviews', data=dict(
            message='foo-message',
            user_id=2,
            stars=5
        ))
        self.assertEqual(xPOST_request.status[:3], '404')

        # test creation of review with all parameters provided in POST request
        # ----------------------------------------------------------------------
        self.subtest_createWithAllParams_proute()

        # test that review ID for sole record in database is correct
        # ----------------------------------------------------------------------
        self.assertEqual(Review.select().get().id, 1)

        # test creatxn of review in all cases of parameter missing in POST req.
        # ----------------------------------------------------------------------
        self.subtest_createWithoutAllParams_proute()

    # def test_list_proute(self):
    #     """
    #     Test proper representation of all place review records upon GET
    #     requests to API.
    #     """
    #     # test response to GET request by place ID which does not exist
    #     # ----------------------------------------------------------------------
    #     GET_request1 = self.app.get('places/1000/reviews')
    #     self.assertEqual(len(json.loads(GET_request1.data)), 404)
    #
    #     # test response to GET request by place ID which exists
    #     # ----------------------------------------------------------------------
    #     GET_request2 = self.app.get('places/1/reviews')
    #     self.assertEqual(len(json.loads(GET_request2.data)), 0)
    #
    #     self.createPlaceReviewViaPeewee()
    #
    #     GET_request3 = self.app.get('places/1/reviews')
    #     self.assertEqual(len(json.loads(GET_request3.data)), 1)
    # #
    # def test_get_proute(self):
    #     """
    #     Test proper representation of a place review record upon GET requests
    #     via review ID to API.
    #     """
    #     # set-up for tests
    #     # ----------------------------------------------------------------------
    #     # create place review records in tables; should have ID's of 1
    #     pr_record = self.createPlaceReviewViaPeewee()
    #     r_record = pr_record.review
    #
    #     # test handling of GET req. for record by place & review IDs which exist
    #     # ----------------------------------------------------------------------
    #     # make GET request for record in table
    #     GET_request1 = self.app.get('/places/1/reviews/1')
    #     GET_data = json.loads(GET_request1.data)
    #
    #     # test that status of response is 200
    #     self.assertEqual(GET_request1.status[:3], '200')
    #
    #     # test that values of response correctly reflect records in database
    #     self.assertEqual(r_record.id, GET_data['id'])
    #     self.assertEqual(r_record.created_at.strftime('%d/%m/%Y %H:%M'), GET_data['created_at'][:-3])
    #     self.assertEqual(r_record.updated_at.strftime('%d/%m/%Y %H:%M'), GET_data['updated_at'][:-3])
    #     self.assertEqual(r_record.message, GET_data['message'])
    #     self.assertEqual(r_record.stars, GET_data['stars'])
    #     self.assertEqual(r_record.user.id, GET_data['from_user_id'])
    #     self.assertEqual(None, GET_data['to_user_id'])
    #     self.assertEqual(ur_record.place.id, GET_data['to_place_id'])
    #
    #     # test handling of GET req. for review record by review ID which exists
    #     # but place ID which does not
    #     # ----------------------------------------------------------------------
    #     GET_request2 = self.app.get('/places/1000/reviews/1')
    #     self.assertEqual(GET_request2.status[:3], '404')
    #
    #     # test handling of GET req. for review record by place ID which exists
    #     # but review id which does not
    #     # ----------------------------------------------------------------------
    #     GET_request2 = self.app.get('/places/1/reviews/1000')
    #     self.assertEqual(GET_request2.status[:3], '404')
    #
    # def test_delete_proute(self):
    #     """
    #     Test deletion of place review records upon DELETE requests to API.
    #     """
    #     # test response to DELETE request for review by review id
    #     # ----------------------------------------------------------------------
    #     self.createPlaceReviewViaPeewee()
    #
    #     GET_request1 = self.app.get('places/1/reviews')
    #     DELETE_request1 = self.app.delete('/places/1/reviews/1')
    #     GET_request2 = self.app.get('places/1/reviews')
    #
    #     num_records_b4 = len(json.loads(GET_request1.data))
    #     num_records_after = len(json.loads(GET_request2.data))
    #
    #     self.assertEqual(DELETE_request1.status[:3], '200')
    #     self.assertEqual(num_records_after, num_records_b4 - 1)
    #
    #     # test handling of DELETE req. for review record by review ID which
    #     # exists but place ID which does not
    #     # ----------------------------------------------------------------------
    #     DELETE_request2 = self.app.delete('/places/1000/reviews/1')
    #     self.assertEqual(DELETE_request2.status[:3], '404')
    #
    #     # test handling of DELETE req. for review record by place ID which
    #     # exists but review ID which does not
    #     # ----------------------------------------------------------------------
    #     DELETE_request2 = self.app.delete('/places/1/reviews/1000')
    #     self.assertEqual(DELETE_request2.status[:3], '404')
