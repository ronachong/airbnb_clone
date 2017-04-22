from flask import Flask
from flask_json import FlaskJSON
from flask_cors import CORS, cross_origin
from config import ORIGINS
import config

__all__ = ["config"]

print "origins is", ORIGINS

# initialize Flask application
app = Flask(__name__)
CORS(app, origins=ORIGINS)

# initialize FlaskJSON instance with Flask app
FlaskJSON(app)
