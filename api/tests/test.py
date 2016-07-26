import unittest
from app import app
from app.views import *

class MyTestClass(unittest.TestCase):

  # initialization logic for the test suite declared in the test module
  # code that is executed before all tests in one test run
  @classmethod
  def setUpClass(cls):
       pass

  # clean up logic for the test suite declared in the test module
  # code that is executed after all tests in one test run
  @classmethod
  def tearDownClass(cls):
       pass

  # initialization logic
  # code that is executed before each test
  def setUp(self):
    '''overload def setUp(self): to create a test client of airbnb app'''
    self.app = app.test_client()
    self.app.testing = True

  # clean up logic
  # code that is executed after each test
  def tearDown(self):
    pass

  # test method
  def test_GET(self):
  	print self.app.get('/').data
