import pytest
from flask import g, session

@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registered'),
))

def test_admin(client, auth):
    assert client.get('/private/admin').status_code == 200
    response = auth.admin()
    assert response.headers["Location"] == "/"

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_admin_validate_input(auth, username, password, message):
    response = auth.admin(username, password)
    assert message in response.data

def test_logout(client, auth):
    auth.admin()

    with client:
        auth.logout()
        assert 'user_id' not in session