from app import app
from app.views import *
from config import HOST, PORT, DEBUG

# run app, but only if this file is being run directly (and not via another file)
if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)
