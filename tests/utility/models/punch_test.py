from datetime import datetime
from sqlite3 import OperationalError
from unittest.mock import call, Mock
import pytest


# Unit under test
from utility import Punch


ALL_BOOLEANS = [(True,), (False,)]


@pytest.fixture()
def connection():
    mock_connection = Mock()
    mock_connection.execute = Mock()
    mock_connection.commit = Mock()
    mock_connection.fetchone = Mock()

    return mock_connection


def test_get_punch_by_id_returns_punch(connection):
    expected = ('some', 'tuple',)
    connection.fetchone.return_value = expected

    punch = Punch(connection)
    actual = punch.get_punch_by_id(1)

    connection.execute.assert_called_once()
    connection.fetchone.assert_called_once()
    assert actual is expected


def test_get_punch_by_id_returns_empty_tuple_on_error(connection):
    connection.execute.side_effect = OperationalError()

    punch = Punch(connection)
    actual = punch.get_punch_by_id(1)

    connection.execute.assert_called_once()
    connection.fetchone.assert_not_called()
    assert actual is ()


@pytest.mark.parametrize("error,action,db_column,expected", [
    # Clock in
    (None, 'in', 'clock_in', True),
    (OperationalError(), 'in', 'clock_in', False),

    # Start Lunch
    (None, 'start', 'lunch_start', True),
    (OperationalError(), 'start', 'lunch_start', False),

    # End Lunch
    (None, 'end', 'lunch_end', True),
    (OperationalError(), 'end', 'lunch_end', False),

    # Clock out
    (None, 'out', 'clock_out', True),
    (OperationalError(), 'out', 'clock_out', False),
])
def test_punch_actions(connection, error, action, db_column, expected):
    id_ = 1
    connection.fetchone.return_value = (id_,)
    connection.execute.side_effect = [None, error]

    punch = Punch(connection)

    punch_time = datetime.now()

    actions = {
        'in': punch.in_,
        'start': punch.start,
        'end': punch.end,
        'out': punch.out,
    }
    actual = actions[action](punch_time)

    if error:
        connection.commit.assert_not_called()
    else:
        connection.commit.assert_called_once()

    expected_sql = 'UPDATE punches SET %s=? WHERE id=?' % (db_column,)
    connection.execute.assert_has_calls(
        [
            call('SELECT * FROM punches ORDER BY id DESC LIMIT 1'),
            call(expected_sql, (punch_time, id_))
        ]
    )

    connection.fetchone.assert_called_once()
    assert actual is expected


def test_insert_new_day_returns_true_on_insert(connection):
    punch = Punch(connection)
    actual = punch.insert_new_day()

    assert actual is True


def test_insert_new_day_returns_false_on_failure(connection):
    connection.execute.side_effect = OperationalError()

    punch = Punch(connection)
    actual = punch.insert_new_day()

    connection.commit.assert_not_called()
    assert actual is False


def test_get_most_recent_day_returns_day(connection):
    # Example of row without punches
    expected = (1, datetime.now(), True)

    connection.fetchone.return_value = expected

    punch = Punch(connection)
    actual = punch.get_most_recent_day()

    sql = 'SELECT * FROM punches ORDER BY id DESC LIMIT 1'
    connection.execute.assert_called_once_with(sql)
    assert actual is expected


def test_get_most_recent_day_returns_empty_tuple_on_error(connection):
    connection.execute.side_effect = OperationalError()

    punch = Punch(connection)

    actual = punch.get_most_recent_day()

    connection.fetchone.assert_not_called()
    assert actual is ()


@pytest.mark.parametrize('expected', ALL_BOOLEANS)
def test_is_work_day_returns_boolean_value(connection, expected):
    punch = Punch(connection)

    # Mocking this public function because it is being tested separately, and
    # we don't want this test dependent on that function.
    punch.get_most_recent_day = Mock(return_value=(1, datetime.now(), expected))

    actual = punch.is_work_day()

    assert actual is expected


@pytest.mark.parametrize('expected_bool', ALL_BOOLEANS)
def test_update_is_work_day_returns_true_on_update(connection, expected_bool):
    punch = Punch(connection)

    expected_id = 1
    # Do not want this test to depend on  get_most_recent_day(),
    # so it is mocked out, as it is tested separately.
    punch.get_most_recent_day = Mock(return_value=(expected_id,))

    actual = punch.update_is_work_day(expected_bool)

    connection.execute.assert_called_once_with(
        'UPDATE punches SET is_work_day=? WHERE id=?',
        (expected_bool, expected_id)
    )
    assert actual is True


def test_update_is_work_day_returns_false_on_failure(connection):
    connection.execute.side_effect = OperationalError()

    punch = Punch(connection)
    # Do not want this test to depend on  get_most_recent_day(),
    # so it is mocked out, as it is tested separately.
    punch.get_most_recent_day = Mock(return_value=(1,))

    actual = punch.update_is_work_day(True)

    connection.commit.assert_not_called()
    assert actual is False
