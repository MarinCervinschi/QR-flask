import pytest
from unittest.mock import patch, MagicMock
from app.db import json_data, query_db

def test_json_data_empty():
    assert json_data(None, None) is None
    assert json_data([], []) is None

def test_json_data_single_row():
    description = [('id',), ('name',)]
    data = [(1, 'Test')]
    expected = [{'id': 1, 'name': 'Test'}]
    assert json_data(description, data) == expected

def test_json_data_multiple_rows():
    description = [('id',), ('name',)]
    data = [(1, 'Test1'), (2, 'Test2')]
    expected = [{'id': 1, 'name': 'Test1'}, {'id': 2, 'name': 'Test2'}]
    assert json_data(description, data) == expected

def test_query_db_success(app):
    with app.app_context():
        with patch('app.db.get_db') as mock_get_db:
            mock_cursor = MagicMock()
            mock_get_db.return_value.cursor.return_value = mock_cursor
            mock_cursor.description = [('id',)]
            mock_cursor.fetchall.return_value = [(1,)]

            result = query_db('SELECT * FROM test')
            assert result == [{'id': 1}]

            mock_cursor.execute.assert_called_once_with('SELECT * FROM test', ())
            mock_cursor.close.assert_called_once()

def test_query_db_failure(app, caplog):
    with app.app_context():
        with patch('app.db.get_db') as mock_get_db:
            mock_cursor = MagicMock()
            mock_get_db.return_value.cursor.return_value = mock_cursor
            mock_cursor.execute.side_effect = Exception("Query error")

            with pytest.raises(Exception, match="Query error"):
                query_db('SELECT * FROM test')

            assert "Query failed" in caplog.text
            mock_cursor.close.assert_called_once()


def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('app.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called