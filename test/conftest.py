import pytest
import pytest_alembic
import subprocess

from pytest_postgresql import factories

from app import app as flaskapp
from config import HOST, PORT


@pytest.fixture(scope="session", autouse=True)
def app():
    """Create and configure a new app instance for each test."""
    flaskapp.host = HOST
    flaskapp.port = PORT
    yield flaskapp


@pytest.fixture
def client(app):
    """A test client for the app."""
    app.testing = True
    yield app.test_client()


@pytest.fixture(scope="session", autouse=True)
def delete_migrations():
    """To delete migration files and folders"""
    print('run')
    subprocess.run(['rm', '-rf', 'migrations'])
    subprocess.run(['rm', '-rf', 'old_migrations'])
    subprocess.run(['find', ' .', '-path "/migrations/.py" -not'
                    ' -name "init.py" -delete'])
    subprocess.run(['find', ' . -path', "/migrations/.pyc", ' -delete'])
    subprocess.run(['git', 'checkout', '-f'])
    subprocess.call('cd ..', shell=True)
    subprocess.run(['rm', ' -rf', '/tmp'])
