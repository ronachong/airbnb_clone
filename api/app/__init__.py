from flask import Flask
from flask_json import FlaskJSON
import config

__all__ = ["config"]

# initialize Flask application
app = Flask(__name__)

# initialize FlaskJSON instance with Flask app
FlaskJSON(app)
