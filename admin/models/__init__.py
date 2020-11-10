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
    connection_name = Column(String(255), nullable=False, unique=True)

    # TODO: make database_name & table combination should be unique
    database_name = Column(String(255), nullable=False, unique=False)
    table = Column(String(255), nullable=False, unique=False)

    # TODO: confirm length for the filter key fields ( and find a better way
    # to store the filter keys keep in mind Arrays are not allowed in SQLite)
    filter_keys = Column(String(255), nullable=False)
    create_dt = Column(DateTime(), server_default=text('CURRENT_TIMESTAMP'))


class Restricted_by_JWT(Base):
    __tablename__ = 'restricted_by_jwt'
    __bind_key__ = 'default'

    id = Column(Integer, primary_key=True)
    connection_name = db.Column(String(255),
                                db.ForeignKey('jwt.connection_name'))
    db_name = Column(String(255), nullable=False)
    restricted_tables = db.Column(String(1000))
