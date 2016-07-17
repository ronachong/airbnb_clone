from app import app
from app.views import *
from app.views import user, state, city, place, place_book, amenity
from config import HOST, PORT, DEBUG

# run app, but only if this file is being run directly (and not via another file)
if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)
