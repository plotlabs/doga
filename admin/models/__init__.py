from sqlalchemy import Integer, String, DateTime, text, Boolean
from sqlalchemy.schema import UniqueConstraint

from app import db

Base = db.Model
Column = db.Column
ForeignKey = db.ForeignKey
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
    """ Defines a table jwt stored in /tmp/test.db to store the table that is
        jwt for the particular connection
    """
    __tablename__ = 'jwt'
    __bind_key__ = 'default'

    id = Column(Integer, primary_key=True)
    jwt_flag = Column(Boolean, nullable=False, unique=False)
    connection_name = Column(String(255), nullable=False, unique=True)

    database_name = Column(String(255), nullable=False, unique=False)
    table = Column(String(255), nullable=False, unique=False)
    UniqueConstraint('database_name', 'table', name='uix_1')

    # confirm length for the filter key fields ( and find a better way
    # to store the filter keys keep in mind Arrays are not allowed in SQLite)

    filter_keys = Column(String(255), nullable=False)
    create_dt = Column(DateTime(), server_default=text('CURRENT_TIMESTAMP'))


class Restricted_by_JWT(Base):
    """ Defines a table Restricted_by_JWT to store the tables restricted by a
    JWT for a particular connection/app
    """
    __tablename__ = 'restricted_by_jwt'
    __bind_key__ = 'default'

    id = Column(Integer, primary_key=True)
    connection_name = Column(String(255), ForeignKey('jwt.connection_name'))
    db_name = Column(String(255), nullable=False)
    restricted_tables = Column(String(1000))


class Deployments(Base):
    """ Defines a table Deployments to store the deployed apps and where they
    have been deployed
    """
    __tablename__ = 'Deployments'
    __bind_key__ = 'default'

    id = Column(Integer, primary_key=True)
    app_name = Column(String(255))
    platfrom = Column(String(255), nullable=False)
    status = Column(String(255), nullable=False)
    # ID of the things & other dicts
    deployment_info = Column(String(1000))


class Relationship(Base):
    """ Defines a table Relationships to store the deployed apps and where they
    have been deployed
    """
    __tablename__ = 'Relationships'
    __bind_key__ = 'default'

    id = Column(Integer, primary_key=True)
    app_name = Column(String(255))
    table1_column = Column(String(255), nullable=False)
    relationship = Column(String(255), nullable=False)
    table2_column = Column(String(255), nullable=False)
