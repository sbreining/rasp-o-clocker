from calendar import month_name
from datetime import datetime
from random import randint
from sqlite3 import OperationalError
from unittest.mock import Mock
from utility import Holiday
import pytest


@pytest.fixture()
def connection():
    connection = Mock()
    connection.commit = Mock()
    connection.execute = Mock()
    connection.fetchall = Mock()
    connection.get_last_row_id = Mock()

    return connection


def test_add_holiday_returns_row_id(connection):
    expected = randint(1, 999)
    connection.get_last_row_id.return_value = expected

    holiday = Holiday(connection)
    actual = holiday.add_holiday(datetime.now())

    connection.execute.assert_called_once()
    connection.commit.assert_called_once()
    connection.get_last_row_id.assert_called_once()
    assert actual is expected


def test_add_holiday_returns_negative_one_on_exception_thrown(connection):
    connection.commit.side_effect = OperationalError()

    holiday = Holiday(connection)
    actual = holiday.add_holiday(datetime.now())

    assert actual is -1


def test_get_row_id_by_date_returns_row_id(connection):
    expected = randint(1,999)
    connection.fetchall.return_value = [(expected,)]

    holiday = Holiday(connection)
    actual = holiday.get_row_id_by_date(datetime.now())

    connection.execute.assert_called_once()
    assert actual is expected


def test_get_row_id_by_date_returns_negative_one_on_exception(connection):
    connection.execute.side_effect = OperationalError()

    holiday = Holiday(connection)
    actual = holiday.get_row_id_by_date(datetime.now())

    assert actual is -1


def test_is_holiday_returns_false_for_no_records_found(connection):
    connection.fetchall.return_value = []

    holiday = Holiday(connection)
    actual = holiday.is_holiday(datetime.now())

    assert actual is False


def test_is_holiday_returns_true_when_finds_record(connection):
    connection.fetchall.return_value = [('some date found',)]

    holiday = Holiday(connection)
    actual = holiday.is_holiday(datetime.now())

    assert actual is True


def test_is_holiday_returns_true_when_exception_thrown(connection):
    connection.fetchall.side_effect = OperationalError()

    holiday = Holiday(connection)
    actual = holiday.is_holiday(datetime.now())

    assert actual is True


def test_remove_holiday_returns_true_on_success(connection):
    holiday = Holiday(connection)
    actual = holiday.remove_holiday(randint(1,999))

    assert actual is True


def test_remove_holiday_returns_false_on_exception_throw(connection):
    connection.commit.side_effect = OperationalError()

    holiday = Holiday(connection)
    actual = holiday.remove_holiday(randint(1,999))

    assert actual is False
