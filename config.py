import os
from dbs import DB_DICT

# Define application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define database configuration
SQLALCHEMY_BINDS = DB_DICT
SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_CONNECT_OPTIONS = {}

JWT_SECRET_KEY = 'jwt-secret-string'

CSRF_ENABLED = True
CSRF_SESSION_KEY = ""
