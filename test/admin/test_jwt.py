import pytest

from test.utils.requests.jwt_tables import invalid_jwt_table


def test_post_jwt(client):
    response = client.post('/admin/content/types', json=invalid_jwt_table)
    # TODO: check if it can be changeed to per database
    assert b'Only one table is allowed to set jwt perdatabase' in response.data


def test_post_jwt_invalid(client):
    invalid_jwt_table['connection_name'] = 'conn'
    response = client.post('/admin/content/types', json=invalid_jwt_table)
    assert b'The database connection given does not exist.' in response.data
