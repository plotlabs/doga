import os
from dbs import DB_DICT

# Define application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define database configuration
SQLALCHEMY_BINDS = DB_DICT
SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_CONNECT_OPTIONS = {}

# Set Host and Port for server
HOST = '0.0.0.0'
PORT = 8080

PROPAGATE_EXCEPTIONS = True

CSRF_ENABLED = True
CSRF_SESSION_KEY = ""

JWTSET = True
JWT_SECRET_KEY = ' x4BlDzv02dKx'
