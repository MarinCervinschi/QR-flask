import pytest
from app.db import query_db

@pytest.mark.parametrize('user_logged_in', [False])
def test_check_admin_redirect(client, user_logged_in):
    if user_logged_in:
        with client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['_fresh'] = True

    response = client.get('/private/dashboard/')
    if not user_logged_in:
        assert response.status_code == 401
        assert b'401' in response.data
    else:
        assert response.status_code == 200


def test_dashboard_render(client, auth):
    auth.admin()
    response = client.get('/private/dashboard/')
    assert response.status_code == 200
    assert b'internal' in response.data
    assert b'http://example.com' in response.data


def test_add_link(client, auth):
    auth.admin()
    response = client.post(
        '/private/dashboard/add', 
        data={'internal': 'internal3', 'external': 'http://example3.com'}
    )
    assert response.status_code == 302 

    with client.application.app_context():
        result = query_db("SELECT * FROM dynamic_links WHERE internal = 'internal3'", one=True)
        assert result is not None
        assert result['external'] == 'example3.com'


def test_add_duplicate_link(client, auth):
    auth.admin()
    response = client.post(
        '/private/dashboard/add', 
        data={'internal': 'internal', 'external': 'http://duplicate.com'},
        follow_redirects=True
    )
    print(response.data)
    assert response.status_code == 500


def test_delete_link(client, auth):
    auth.admin()
    response = client.post('/private/dashboard/delete', data={'id': '1'})
    assert response.status_code == 302

    with client.application.app_context():
        result = query_db("SELECT * FROM dynamic_links WHERE id = 1", one=True)
        assert result is None

def test_edit_link(client, auth):
    auth.admin()
    response = client.post(
        '/private/dashboard/edit', 
        data={'id': '1', 'external': 'http://newexample.com'}
    )
    assert response.status_code == 302

    with client.application.app_context():
        result = query_db("SELECT * FROM dynamic_links WHERE id = 1", one=True)
        assert result['external'] == 'http://newexample.com'

def test_generate_qr_code(client, auth):
    auth.admin()
    response = client.post('/private/dashboard/qr', data={'id': '1'})
    assert response.status_code == 200
    assert response.mimetype == 'image/png'


def test_generate_qr_code_invalid_id(client, auth):
    auth.admin()
    response = client.post('/private/dashboard/qr', data={'id': '999'})
    assert response.status_code == 500