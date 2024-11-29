import pytest
from flask import g, session

@pytest.mark.parametrize(('username', 'password', 'message', 'status_code'), (
    ('', '', b'Incorrect username.', 401),
    ('invalid_user', 'password', b'Incorrect username.', 401),
    ('test', 'wrongpassword', b'Incorrect password.', 401), 
))
def test_admin_validate_input(client, username, password, message, status_code):
    response = client.post('/private/admin', data={'username': username, 'password': password})
    assert message in response.data
    assert response.status_code == status_code

def test_admin_success(client, auth):
    response = auth.admin()

    assert response.status_code == 302
    assert response.headers["Location"] == "/private/dashboard/"

    with client:
        client.get('/private/admin')

        assert session['user_id'] is not None
        assert g.user['username'] == 'test'

def test_admin_already_logged_in(client, auth):
    auth.admin()

    with client:
        response = client.get('/private/admin')

        assert response.status_code == 302
        assert response.headers["Location"] == "/private/dashboard/"

def test_logout(client, auth):
    auth.admin()

    with client:
        auth.logout()
        # Verify session is cleared
        assert 'user_id' not in session
        response = client.get('/private/admin/')
        assert b'Incorrect username.' not in response.data