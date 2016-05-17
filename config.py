import os

import psycopg2
import urlparse



WTF_CSRF_ENABLED = True
SECRET_KEY = 'capstoneproj'

#the updates databases are below
SQLALCHEMY_DATABASE_URI='postgresql://capstoneproject:success@localhost/capstonedb' 