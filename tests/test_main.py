import pytest

@pytest.fixture
def mock_query_db(mocker):
    return mocker.patch('app.db.query_db') 

def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'<!DOCTYPE html>' in response.data


@pytest.mark.parametrize('dynamic_string, query_result, expected_redirect', [
    ('internal', {'external': 'www.example.com'}, 'http://example.com'), 
    ('invalid', None, None),
])
def test_custom_route(client, mock_query_db, dynamic_string, query_result, expected_redirect):
    mock_query_db.return_value = query_result

    response = client.get(f'/{dynamic_string}')

    if query_result:
        assert response.status_code == 302
        assert response.headers['Location'] == expected_redirect
    else:
        assert response.status_code == 404
        assert b"404" in response.data


def test_custom_route_db_error(client, mock_query_db):
    mock_query_db.side_effect = Exception("Database error")

    response = client.get('/test_error')

    assert response.status_code == 404
    assert b"<!DOCTYPE html>" in response.data


def test_404_error_handler(client):
    response = client.get('/nonexistent_route')
    assert response.status_code == 404
    assert b"<!DOCTYPE html>" in response.data