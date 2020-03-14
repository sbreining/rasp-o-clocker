from utility import Database
from unittest.mock import Mock, patch
import sqlite3
import pytest


cursor = Mock()
cursor.execute = Mock()
cursor.fetchall = Mock()
cursor.fetchone = Mock()

connection = Mock()
connection.commit = Mock()
connection.cursor = Mock(return_value=cursor)


def test_commit():
    with patch.object(sqlite3, 'connect', return_value=connection):
        db = Database(Mock())
        db.commit()

    connection.commit.assert_called_once()


@pytest.mark.parametrize('sql,data', [('some sql', (1,)), ('more sql', None)])
def test_execute(sql, data):
    with patch.object(sqlite3, 'connect', return_value=connection):
        db = Database(Mock())
        if data is not None:
            db.execute(sql, data)
        else:
            db.execute(sql)

    if data is not None:
        cursor.execute.assert_called_once_with(sql, data)
        # Need to reset the mock for the second test run.
        cursor.execute.reset_mock()
    else:
        cursor.execute.assert_called_once_with(sql, ())


def test_fetchall():
    expected = [(1,), (2,)]
    cursor.fetchall.return_value = expected
    with patch.object(sqlite3, 'connect', return_value=connection):
        db = Database(Mock())
        actual = db.fetchall()

    cursor.fetchall.assert_called_once()
    assert actual is expected


def test_fetchone():
    expected = (1,)
    cursor.fetchone.return_value = expected
    with patch.object(sqlite3, 'connect', return_value=connection):
        db = Database(Mock())
        actual = db.fetchone()

    cursor.fetchone.assert_called_once()
    assert actual is expected


def test_get_last_row_id():
    expected = 123
    cursor.lastrowid = expected
    with patch.object(sqlite3, 'connect', return_value=connection):
        db = Database(Mock())
        actual = db.get_last_row_id()

    assert actual is expected