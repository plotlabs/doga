"""Tests for the /admin/content endpoint
"""
import os

import pytest
import json

from flask_testing import TestCase

from test.utils.assertions import assert_valid_schema, load_json
from test.utils.requests.admin import admin
import test.utils.requests.test_content as requests
import test.utils.requests.sqlite_content as sqlite_request
from test.utils.requests.dbinit_sqlite import dbinit_sqlite

from . import headers, endpoints


@pytest.mark.usefixtures('client')
class Test_Content:

    def test_setup(self, client):
        client.post('/admin/admin_profile',
                    json=admin)

        if 'name' in admin:
            del admin['name']

        response = client.post('/admin/login', json=admin)
        headers['Authorization'] = 'Bearer ' + response.json['access_token']

    def test_get_no_content(self, client):
        response = client.get('/admin/content/types/nocontent',
                              headers=headers)
        assert b'URL was not found' in response.data

    def test_post_content(self, client):
        response = client.post(
            'admin/content/types',
            json=requests.invalid_boolean_column,
            headers=headers)
        assert b'Boolean datatype for columns is not supported by default '
        b'database connection.' in response.data

    def test_mysql_constraint_unique(self, client):
        response = client.post('admin/content/types',
                               json=sqlite_request.invalid_constraint_unique,
                               headers=headers)
        assert b'Unique constraint on TEXT column type'
        b'is not allowed for mysql database.' in response.data

    def test_post_valid_content(self, client):
        data = load_json('test_content_valid.json')
        response = client.post('admin/content/types',
                               json=data,
                               headers=headers)
        assert b'Success' in response.data

    def test_retreive_content(self, client):
        response = client.get('admin/content/types/test/test_table',
                              headers=headers)
        assert b'No matching content found' in response.data


"""
def test_invalid_filterkey(client):
    client.post('/admin/dbinit', json=dbinit_sqlite)
    response = client.post('admin/content/types',
                           json=requests.invalid_filter_keys)
    assert b'Only column names are allowed in filter keys.' in response.data


def test_invalid_colum_type(client):
    client.post('/admin/dbinit', json=dbinit_sqlite)
    response = client.post('admin/content/types',
                           json=requests.invalid_colum_type)
    assert b'Invalid column type for column id.' in response.data
"""


"""TODO: put this in a calss
def test_add_content(client):
    data = load_json('table_content.json')
    response = client.post('test/test_table', json=data)
    assert b"asdadsasd" in response.data
"""
