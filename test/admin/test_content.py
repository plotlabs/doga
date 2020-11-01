"""Tests for the /admin/content endpoint
"""
import os

import pytest
import json

from test.utils.assertions import assert_valid_schema, load_json
import test.utils.requests.test_content as requests
import test.utils.requests.sqlite_content as sqlite_request
from test.utils.requests.dbinit_sqlite import dbinit_sqlite


def test_no_admin(client):
    response = client.get('/admin/admin_profile/testnoadmin@temp.com')
    assert b'Admin does not exist.' in response.data


def test_get_no_content(client):
    response = client.get('/admin/content/types/nocontent')
    assert b'URL was not found' in response.data


def test_post_content(client):
    response = client.post(
        'admin/content/types',
        json=requests.invalid_boolean_column)
    assert b'Boolean datatype for columns is not supported by default '
    b'database connection.' in response.data


def test_mysql_constraint_unique(client):
    response = client.post('admin/content/types',
                           json=sqlite_request.invalid_constraint_unique)
    assert b'Unique constraint on TEXT column type'
    b'is not allowed for mysql database.' in response.data


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


def test_post_valid_content(client):
    data = load_json('test_content_valid.json')
    response = client.post('admin/content/types', json=data)
    assert b'Success' in response.data


def test_retreive_content(client):
    response = client.get('admin/content/types/test/test_table')
    assert b'No matching content found' in response.data


"""TODO: put this in a calss
def test_add_content(client):
    data = load_json('table_content.json')
    response = client.post('test/test_table', json=data)
    assert b"asdadsasd" in response.data
"""
