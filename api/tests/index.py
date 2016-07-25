import unittest
from app import app
from json import loads
from datetime import datetime

# validates GET request to index returns 200, JSON status is OK, and time codes

class indexTestCase(unittest.TestCase):
  def setUp(self):
    '''overload def setUp(self): to create a test client of airbnb app'''
    self.app = app.test_client()
    self.app.testing = True

  def test_200(self):
    '''validate if the status code of a request on GET / is 200'''
    GETstatus = self.app.get('/').status
    self.assertEqual(GETstatus[:3], '200')

  def test_status(self):
    '''validate if the key status of the response to a request on GET / has the value OK'''
    GETdata = loads(self.app.get('/').data)
    self.assertEqual(GETdata['status'], 'OK')

  def test_time(self):
    ''' validate value for key 'time' of JSON response to a GET request / is equal
    to time "now" via datetime.now (checking only: year, month, day, hour and minute) '''
    GETdata = loads(self.app.get('/').data)
    now = datetime.now().strftime('%d/%m/%Y %H:%M')
    self.assertEqual(GETdata['time'][:-3], now)

  def test_time_utc(self):
    ''' validate value for key 'utc_time' of JSON response to a GET request / is equal
    to time "now" via datetime.now (checking only: year, month, day, hour and minute) '''
    GETdata = loads(self.app.get('/').data)
    now = datetime.utcnow().strftime('%d/%m/%Y %H:%M')
    self.assertEqual(GETdata['utc_time'][:-3], now)
