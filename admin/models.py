from sqlalchemy import Integer, String, DateTime, text, Boolean

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


class JWT(Base):
    __tablename__ = 'jwt'
    __bind_key__ = 'default'

    id = Column(Integer, primary_key=True)
    jwt_flag = Column(Boolean, nullable=False, unique=False)
    table = Column(String(255), nullable=False, unique=True)
    database_name = Column(String(255), nullable=False, unique=True) 
    create_dt = Column(DateTime(), server_default=text('CURRENT_TIMESTAMP'))
