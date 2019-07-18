from sqlalchemy import *

from app import db

Base = db.Model
Column = db.Column
metadata = db.metadata
relationship = db.relationship


