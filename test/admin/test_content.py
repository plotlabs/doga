"""Tests for the /admin/content endpoint
"""
import os

import pytest
import json

from flask_testing import TestCase

from test.utils.assertions import assert_valid_schema, load_json
from test.utils.requests.admin import admin
from test.utils.requests.test_content import *
import test.utils.requests.sqlite_content as sqlite_request
from test.utils.requests.dbinit_sqlite import dbinit_sqlite

from . import headers, endpoints


@pytest.mark.usefixtures('client')
class Test_Content:
    """Tests post valid contet table, retreive it and add content to it.
       * database tested : SQLite
    """

    def test_setup(self, client):
        client.post('/admin/admin_profile', json=admin)

        if 'name' in admin:
            del admin['name']

        response = client.post('/admin/login', json=admin)
        headers['Authorization'] = 'Bearer ' + response.json['access_token']

    def test_get_no_content(self, client):
        response = client.get('/admin/content/types/nocontent',
                              headers=headers)
        assert b'URL was not found' in response.data

    def test_post_valid_content(self, client):
        response = client.post('admin/content/types',
                               json=valid_content,
                               headers=headers)
        assert b'Success' in response.data

    def test_retreive_content_empty(self, client):
        response = client.get('admin/content/types',
                              headers=headers)
        assert b'No apps and content created yet.' in response.data


"""Tests to check that the admin model's constraints at endpoint:
   `admin/content/types`
"""


def test_invalid_table_name(client):
    """Test POST 'admin/content/types' endpoint password constraints,
       0 < password < , and not None
    """
    invalid_table_name = valid_content

    invalid_table_name['table_name'] = None
    response = client.post('admin/content/types', json=invalid_table_name,
                           headers=headers)
    assert b'must not be `None`' in response.data

    invalid_table_name['table_name'] = "   "
    response = client.post('admin/content/types', json=invalid_table_name,
                           headers=headers)
    assert b'must contain characters' in response.data

    invalid_table_name['table_name'] = 'veryveryveryveryveryveryveryveryverylongname'  # noqa 401
    response = client.post('admin/content/types', json=invalid_table_name,
                           headers=headers)
    assert b'less than or equal to `32`.' in response.data


"""
def test_invalid_filterkey(client):
    response = client.post('/admin/dbinit', json=dbinit_sqlite,
                           headers=headers)

    response = client.post('admin/content/types',
                           json=invalid_filter_keys,
                           headers=headers)
    assert b'Only column names are allowed in filter keys.' in response.data
"""


def test_invalid_colum_type(client):
    client.post('/admin/dbinit', json=dbinit_sqlite, headers=headers)
    response = client.post('admin/content/types',
                           json=invalid_colum_type,
                           headers=headers)
    assert b'Invalid column type for column desc.' in response.data


def test_invalid_column_boolean(client):
    response = client.post(
        'admin/content/types',
        json=invalid_boolean_column,
        headers=headers)
    assert b'Boolean datatype for columns is not supported by default database connection.' in response.data  # noqa 401


"""
def test_mysql_constraint_unique(client):
    response = client.post('admin/content/types',
                           json=sqlite_request.invalid_constraint_unique,
                           headers=headers)
    assert b'Unique constraint on TEXT column type is not allowed for mysql database.' in response.data  # noqa 401
"""
