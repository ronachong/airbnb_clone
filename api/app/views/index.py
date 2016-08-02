from datetime import datetime
from pytz import utc, timezone

from flask_json import json_response
from peewee import *

from app import app, models


@app.route('/', methods=['GET'])
def index():
    """Serve a simple hash for any requests to / with status 200."""
    return json_response(
        status="OK",
        utc_time=datetime.utcnow().strftime('%d/%m/%Y %H:%M:%S'),
        time=utc_to_local(datetime.utcnow()).strftime('%d/%m/%Y %H:%M:%S')
    )


@app.errorhandler(404)
def not_found(e):
    """Serve a 404, not found json for any requests to / with status 404."""
    return json_response(
        add_status_=False,
        status_=404,
        code=404,
        msg="not found"
    )


def utc_to_local(utc_dt):
    """Convert a utc date time to the specified local timezone local_tz."""
    local_tz = timezone('America/Los_Angeles')
    local_dt = utc_dt.replace(tzinfo=utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)


def before_request():
    """Connect to airbnb_test to prior to each request."""
    models.database.connect()


def after_request():
    """Close connection to the database after each request."""
    models.database.close()
