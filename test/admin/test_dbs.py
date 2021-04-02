import subprocess
import pytest

from flask_testing import TestCase
from sqlalchemy import create_engine

from test.utils.assertions import assert_valid_schema, load_json
from test.utils.requests.dbinit_sqlite import *
from test.utils.requests.admin import admin

from . import headers, endpoints


@pytest.mark.usefixtures('client')
class Test_DBinit:

    def test_setup(self, client):
        client.post('/admin/admin_profile', json=admin)

        if 'name' in admin:
            del admin['name']

        response = client.post('/admin/login', json=admin)
        headers['Authorization'] = 'Bearer ' + response.json['access_token']

    @classmethod
    def teardown_class(cls):
        print("delete app & remove all changes to app")
        subprocess.run(["git", "clean", "-df"])

    def test_dbinit(self, client):
        response = client.post(endpoints['db_init'], json=dbinit_sqlite,
                               headers=headers)
        assert b'Successfully created database connection string.'\
            in response.data

    def test_dbinit_repeated(self, client):

        response = client.post(endpoints['db_init'], json=dbinit_sqlite,
                               headers=headers)
        assert b'Connection with name: tmp is already present. '
        b'Use a different name.' in response.data

    def test_dbinit_repeatedDB(self, client):

        response = client.post(endpoints['db_init'],
                               json=dbinit_sqlite2,
                               headers=headers)  # noqa 401
        assert b'Successfully created database connection string.'\
            in response.data
