"""Tests for the /admin/content endpoint
"""
import os

import pytest
import json

from test.utils.assertions import assert_valid_schema, load_json


def test_no_admin(client):
    response = client.get('/admin/admin_profile/testnoadmin@temp.com')
    assert b'Admin does not exist.' in response.data


def test_get_content(client):
    response = client.get('/admin/content/types')
    assert_valid_schema(json.loads(response.data), 'content_types.json')


def test_get_no_content(client):
    response = client.get('/admin/content/types/nocontent')
    assert b'URL was not found' in response.data


def test_post_content(client):
    data = load_json('test_content.json')
    response = client.post('admin/content/types', json=data)
    assert b'Boolean datatype for columns is not supported by default '
    b'database connection.' in response.data
