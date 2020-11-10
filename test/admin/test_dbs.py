import subprocess

from flask_testing import TestCase
from sqlalchemy import create_engine

from test.utils.assertions import assert_valid_schema, load_json
from test.utils.requests.dbinit_sqlite import dbinit_sqlite


class Test_dbinit:

    @classmethod
    def teardown_class(cls):
        print("delete app & remove all changes to app")
        subprocess.run(["git", "clean", "-df"])

    def test_dbinit(self, client):
        response = client.post('/admin/dbinit', json=dbinit_sqlite)
        assert b'Successfully created database connection string.'\
            in response.data

    def test_dbinit_repeated(self, client):

        response = client.post('/admin/dbinit', json=dbinit_sqlite)
        assert b'Connection with name: tmp is already present. '
        b'Use a different name.' in response.data

    def test_dbinit_repeatedDB(self, client):

        data = load_json('dbinit_sqlite2.json')
        response = client.post('/admin/dbinit', json=data)
        assert b'Successfully created database connection string.'\
            in response.data
