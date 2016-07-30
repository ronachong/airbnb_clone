import json
import unittest
from datetime import datetime

from app import app
from app.views import index


# validates GET request to index returns 200, JSON status is OK, and time codes


class indexTestCase(unittest.TestCase):
    def setUp(self):
        """
        Overload def setUp(self): to create a test client of airbnb app, and
        create amenity table in airbnb_test database.
        """
        self.app = app.test_client()    # set up test client
        self.app.testing = True         # set testing to True

    def test_200(self):
        """
        Validate if the status code of a request on GET / is 200.
        """
        result = self.app.get('/')

        GETstatus_code = self.app.get('/').status_code
        self.assertEqual(GETstatus_code, 200)

    def test_status(self):
        """
        Validate if the key status of the response to a request on GET / has
        the value OK.
        """
        GETdata = json.loads(self.app.get('/').data)
        self.assertEqual(GETdata['status'], 'OK')

    def test_time(self):
        """
        Validate value for key 'time' of JSON response to a GET request / is
        equal to time "now" via datetime.now (checking only: year, month, day,
        hour and minute.
        """
        GETdata = loads(self.app.get('/').data)
        now = datetime.now().strftime('%d/%m/%Y %H:%M')
        self.assertEqual(GETdata['time'][:-3], now)

    def test_time_utc(self):
        """
        Validate value for key 'utc_time' of JSON response to a GET request /
        is equal to time "now" via datetime.now (checking only: year, month,
        day, hour and minute).
        """
        GETdata = loads(self.app.get('/').data)
        now = datetime.utcnow().strftime('%d/%m/%Y %H:%M')
        self.assertEqual(GETdata['utc_time'][:-3], now)
