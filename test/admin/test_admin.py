"""Tests for the /admin endpoint
"""
import json
import pytest

from test.utils.assertions import assert_valid_schema, load_json


def test_no_admin(client):
    response = client.get('/admin/admin_profile/testnoadmin@temp.com')
    assert b'Admin does not exist.' in response.data


def test_add_admin(client):
    admin = load_json('admin.json')
    client.post('/admin/admin_profile', json=admin)
    response = client.get('/admin/admin_profile/testadmin@plotlabs.com')
    assert_valid_schema(json.loads(response.data), 'admin_schema.json')


def test_login_admin(client):
    admin = load_json('admin.json')
    client.post('/admin/admin_profile', json=admin)

    if 'name' in admin:
        del admin['name']

    response = client.post('/admin/login', json=admin)
    assert b'Successfully logged in' in response.data
