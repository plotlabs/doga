from sqlalchemy import *

from app import db

Base = db.Model
Column = db.Column
metadata = db.metadata
ForeignKey = db.ForeignKey
relationship = db.relationship
