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

    with client.session_transaction() as sess:
        assert sess['user_id'] == 1
        assert sess.permanent is True

def test_admin_already_logged_in(client, auth):
    auth.admin()

    response = client.get('/private/admin')

    assert response.status_code == 302
    assert response.headers["Location"] == "/private/dashboard/"

def test_logout(client, auth):
    auth.admin()
    response  = auth.logout()

    with client.session_transaction() as sess:
        assert response.status_code == 302
        assert response.headers["Location"] == "/private/admin"
        
        assert 'user_id' not in sess
        response = client.get('/private/dashboard/')
        assert response.status_code == 401