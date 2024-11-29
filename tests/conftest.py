import os
import tempfile

import pytest
from app import create_app
from app.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

def init_test_db():
    init_db()
    try:
        db_test = get_db()
        cur = db_test.cursor()
        for command in _data_sql.split(';'):
            if command.strip():
                cur.execute(command)
        
        db_test.commit()
    except Exception as e:
        db_test.rollback()
        app.logger.error(f"Failed to initialize the database: {e}")
        raise
    finally:
        cur.close()

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_test_db()

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def admin(self, username='test', password='test'):
        return self._client.post(
            '/private/admin',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.post('/private/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)