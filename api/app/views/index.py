from flask_json import FlaskJSON, json_response
from datetime import datetime, tzinfo
from pytz import utc, timezone
from app import app, models
from peewee import *

local_tz = timezone('America/Los_Angeles')

@app.route('/', methods=['GET'])
def index():
    ''' index serves a hash with the status ok and local and utc times for any quests with status 200 '''
    return json_response(status="OK", utc_time=datetime.utcnow().strftime('%m/%d/%Y %H:%M:%S'), time=utc_to_local(datetime.utcnow()).strftime('%m/%d/%Y %H:%M:%S')) #format 2nd arg into UTC

@app.errorhandler(404)
def not_found(e):
    ''' not_found serves a json hash with code 404 and msg "not found" for any requests with status 404 '''
    return json_response(add_status_=False, code=404, msg="not found")

def utc_to_local(utc_dt):
    ''' utc_to_local converts a utc date time to the specified local timezone local_tz '''
    local_dt = utc_dt.replace(tzinfo=utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)

def before_request():
    ''' before_request specifies that the database should be connected to rior to each request '''
    models.database.connect()

def after_request():
    ''' after_request specifies that the connection to the database should be closed after each request '''
    models.database.close()
