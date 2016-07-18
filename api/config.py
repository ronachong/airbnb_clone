import os

env = os.environ.get('AIRBNB_ENV')

if env == 'development':
    # assign specs for dev env
    # os.environ['AIRBNB_DATABASE_PWD_DEV'] = 'wrdev' | this only sets env var in current shell; currently setting var permanently for own user via ~/.bash_profile
    DEBUG = True
    HOST = 'localhost'
    PORT = 3333
    DATABASE = { 'host': '158.69.79.94',
                 'user': 'airbnb_user_dev',
                 'database': 'airbnb_dev',
                 'port': 3306,
                 'charset': 'utf8',
                 'password': os.environ.get('AIRBNB_DATABASE_PWD_DEV') }

elif env == 'production':
    # assign specs for prod env
    # os.environ['AIRBNB_DATABASE_PWD_PROD'] = 'wrprod' | this only sets env var in current shell; currently setting var permanently for admin user via ~/.bash_profile
    DEBUG = False
    HOST = '0.0.0.0'
    PORT = 3000
    DATABASE = { 'host': '158.69.79.94',
                 'user': 'airbnb_user_prod',
                 'database': 'airbnb_prod',
                 'port': 3306,
                 'charset': 'utf8',
                 'password': os.environ.get('AIRBNB_DATABASE_PWD_PROD') }

elif env == 'test':
   # assign specs for test env
   # os.environ['AIRBNB_DATABASE_TEST'] = 'testpw' | this only sets env var in current shell; currently setting var permanently for admin user via ~/.bash_profile
   DEBUG = False
   HOST = 'localhost'
   PORT = 5555
   DATABASE = { 'host': '158.69.79.94',
                'user': 'airbnb_user_test',
                'database': 'airbnb_test',
                'port': 3306,
                'charset': 'utf8',
                'password': os.environ.get('AIRBNB_DATABASE_TEST') }
