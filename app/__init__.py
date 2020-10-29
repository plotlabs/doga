import time

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from app.utils import migrate as run_migration

# Define application object
app = Flask(__name__)

# Define app configuration
app.config.from_pyfile("../config.py")

db = SQLAlchemy(app)

# Import all the blueprints
from .blueprints import *

migrate = Migrate(app, db)

jwt = JWTManager(app)


@app.after_request
def after_request(response):
    response.headers.set('Access-Control-Allow-Origin',
                         '*')
    response.headers.add("Access-Control-Allow-Headers",
                         "x-requested-with, Content-Type, authorization")
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response


@app.teardown_request
def teardown(request):
    time.sleep(0.5)
    run_migration()


@app.teardown_request
def teardown(request):
    time.sleep(0.5)
    run_migration()


CORS(app, supports_credentials=True)
