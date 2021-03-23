from sqlalchemy import *
from flask_sqlalchemy import SQLAlchemy

from app import db, app

Base = db.Model
Column = db.Column
metadata = db.metadata
relationship = db.relationship


class AlembicVersionDefault(Base):
    __tablename__ = 'alembic_version'
    __bind_key__ = 'default'
    version_num = Column(String(32), primary_key=True)

test = SQLAlchemy(app)
Base_test = test.Model
Columntest = test.Column


class AlembicVersionTest(Base_test):
    __tablename__ = 'alembic_version'
    __bind_key__ = 'test'
    version_num = Columntest(String(32), primary_key=True)

