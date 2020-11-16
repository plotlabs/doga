"""Tests for the /admin endpoint
"""
import json
import pytest


from test.utils.assertions import assert_valid_schema, load_json
from test.utils.requests.admin import *

from . import headers, endpoints


def test_login_admin(client):
    """Test post a valid admin object and login, store the jwt created
    """

    client.post('/admin/admin_profile', json=admin)

    if 'name' in admin:
        name = admin['name']
        del admin['name']

    response = client.post('/admin/login', json=admin)
    headers['Authorization'] = 'Bearer ' + response.json['access_token']
    admin['name'] = name
    assert b'Successfully logged in' in response.data


def test_add_admin(client):
    """Test the schema of the response for the response
    """
    client.post('/admin/admin_profile', json=admin)
    response = client.get('/admin/admin_profile/testadmin@plotlabs.com',
                          headers=headers)
    assert_valid_schema(json.loads(response.data), 'admin_schema.json')


def test_no_admin(client):
    """Test a GET admin for admin not present at '/admin/admin_profile/<email>'
    """
    response = client.get('/admin/admin_profile/testnoadmin@temp.com',
                          headers=headers)
    assert b'Admin does not exist.' in response.data


def test_valid_admin(client):
    """Test in GET admin return correct admin value
    """
    admin_email = admin['email']
    response = client.get('/admin/admin_profile/'+admin_email,
                          headers=headers).json['result']
    assert admin_email == response['email']
    assert admin['name'] == response['name']
    assert response['id'] is not None


"""Tests to check that the admin model's constraints at endpoint:
   `amdin/admin_profile`
"""


def test_admin_password_checks(client):
    """Test POST 'admin/admin_profile' endpoint password constraints,
       6 < password < 32, and not None
    """
    response = client.post('/admin/admin_profile', json=admin_password_long)
    assert b'less than or equal to `32`.' in response.data

    response = client.post('/admin/admin_profile', json=admin_password_short)
    assert b'greater than or equal to `6`' in response.data

    response = client.post('admin/admin_profile', json=admin_password_none)
    assert b'must not be `None`' in response.data


def test_admin_email_check(client):
    """Test POST 'amdin/admin_profile' endpoint `email` constraints,
       email must be in a regex format with @ and . before co/com/in ...
       email must not be None
    """
    response = client.post('/admin/admin_profile', json=admin_invalid_email_format)  # noqa 401
    assert b'Invalid email id, please re-enter a valid email' in response.data

    response = client.post('/admin/admin_profile', json=admin_email_none)
    assert b'must not be `None`.' in response.data


def test_admin_name_check(client):
    """Test POST 'admin/admin_profile' endpoint 'name' constraints,
       4 < name < 32, and not None
    """
    response = client.post('/admin/admin_profile', json=admin_name_short)
    assert b'Invalid value for `name`, length must be greater' in response.data

    response = client.post('/admin/admin_profile', json=admin_name_long)
    assert b'Invalid value for `name`, length must be less' in response.data
