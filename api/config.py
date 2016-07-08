import os

env = os.environ.get('AIRBNB_ENV')

dev_db_hash = {'host': '158.69.79.94',
               'user': 'airbnb_user_dev',
               'database': 'airbnb_dev',
               'port': '3306',
               'charset': 'utf8',
               'password': 'wrdev'}

prod_db_hash = {'host': '158.69.79.94',
                'user': 'airbnb_user_prod',
                'database': 'airbnb_prod',
                'port': '3306',
                'charset': 'utf8',
                'password': 'wrprod'}

dev_envs = {'DEBUG': 'True', 'HOST': 'localhost', 'PORT': '3333', 'DATABASE': dev_db_hash}
prod_envs = {'DEBUG': 'False', 'HOST': '0.0.0.0', 'PORT': '3000', 'DATABASE': prod_db_hash}

if env == 'development':
    # assign specs for dev env
    for key in dev_envs.keys(): os.environ[key] = dev_envs[key]

elif env == 'production':
    # assign specs for prod env
    for key in prod_envs.keys(): os.environ[key] = prod_envs[key]
