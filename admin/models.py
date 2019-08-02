from sqlalchemy import Integer, String, DateTime, text

from app import db

Base = db.Model
Column = db.Column
metadata = db.metadata
relationship = db.relationship


class Admin(Base):
    __tablename__ = 'admin'
    __bind_key__ = 'default'

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False, unique=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255))
    create_dt = Column(DateTime(), server_default=text('CURRENT_TIMESTAMP'))
