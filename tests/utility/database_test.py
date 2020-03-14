from utility import Database
from unittest.mock import Mock, patch


@patch('sqlite3.connect')
def test_commit(connect):
    connection = Mock()
    connection.commit = Mock()
    connect.return_value = connection

    db = Database(Mock())
    db.commit()

    connection.commit.assert_called_once()
