'''validates that GET to index returns 200, JSON status is OK, and time codes'''
import os
import flaskr
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):
  def setUp(self):
  '''overload def setUp(self): to create a test client of app'''
  
  def test_status(self):
  '''validate if the key status of the JSON response of a request on GET / is equal of OK'''
  def test_time(self):
  '''validate if the key time of the JSON response of a request on GET / is equal of now (only: year, month, day, hour and minute)'''
  def test_time_utc(self):
  '''validate if the key utc_time of the JSON response of a request on GET / is equal of now (only: year, month, day, hour and minute)'''
