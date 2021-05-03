from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from sqlalchemy import BLOB
from sqlalchemy import event
from app.types import ImageType
from sqlalchemy import Table

# Define application object
app = Flask(__name__)

# Define app configuration
app.config.from_pyfile("../config.py")

db = SQLAlchemy(app)

# Import all the blueprints
from .blueprints import *  # noqa 402

migrate = Migrate(app, db)

jwt = JWTManager(app)


@event.listens_for(Table, "column_reflect")
def _setup_imgtype(inspector, table, column_info):
    if isinstance(column_info["type"], BLOB):
        try:
            column_info["type"] = ImageType()
        except Exception:
            pass


@app.after_request
def after_request(response):
    response.headers.set('Access-Control-Allow-Origin',
                         '*')
    response.headers.add("Access-Control-Allow-Headers",
                         "x-requested-with, Content-Type, authorization")
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response


CORS(app, supports_credentials=True)

db.create_all()
