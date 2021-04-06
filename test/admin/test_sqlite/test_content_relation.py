import subprocess
import pytest
import json

from flask_testing import TestCase
from sqlalchemy import create_engine

from test.utils.assertions import assert_valid_schema, load_json
from test.utils.requests.dbinit_sqlite import *
from test.utils.requests.admin import admin
from test.utils.requests.sqlite_content import *
from test.admin import headers, endpoints

from test.conftest import ResponsesStored


@pytest.mark.usefixtures('client')
class Test_RelatedContent:

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

    # create a new sqlite db
    def test_dbinit(self, client):
        response = client.post(endpoints['db_init'], json=dbinit_sqlite,
                               headers=headers)
        assert b'Successfully created database connection string.'\
            in response.data

    # get allowed types of content
    def test_create_content(self, client):
        response = client.get(endpoints['column_types'],
                              headers=headers)
        ResponsesStored.allowed_types = json.loads(response.data)['result']
        assert 200 == response.status_code

    # post tables to create data
    def test(self, client):

        content_def["columns"] = []
        for _type in ResponsesStored.allowed_types:
            content_def["columns"].append(columns_with_defaults[_type])

        response = client.post(endpoints['admin_content'],
                               json=content_def,
                               headers=headers)  # noqa 401
        assert b'Successfully created module.'\
            in response.data

    # add a one-one relateion

    # test out the relation by adding values

    # success
