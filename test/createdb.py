import pytest
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


@pytest.fixture(scope='function')
def setup_database():

    engine = create_engine('sqlite://')
    declarative_base().metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    yield session
    session.remove()
    session.delete()
