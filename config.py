import os

# Define application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define database configuration
SQLALCHEMY_DATABASE_URI = os.getenv("DB_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_CONNECT_OPTIONS = {}

CSRF_ENABLED = True
CSRF_SESSION_KEY = ""