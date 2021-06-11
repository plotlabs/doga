from sqlalchemy import *
from app import db

Base = db.Model
Column = db.Column
metadata = db.metadata
relationship = db.relationship


class AlembicVersionDefault(Base):
    __tablename__ = "alembic_version"
    __bind_key__ = "default"
    version_num = Column(String(32), primary_key=True)
