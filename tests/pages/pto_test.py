from datetime import datetime
from pages import PaidTimeOff
from unittest.mock import Mock, patch


def driver(status):
    table = Mock(text='01/01/01 x 8 x %s x' % status)

    parent_element = Mock()
    parent_element.click = Mock()
    parent_element.find_element_by_class_name = Mock(return_value=table)

    nav_bar_element = Mock()
    nav_bar_element.click = Mock()

    driver_mock = Mock()
    driver_mock.find_element_by_id = Mock(return_value=parent_element)
    driver_mock.find_element_by_class_name = Mock(return_value=nav_bar_element)

    return driver_mock


def test_is_pto_day_returns_false_when_request_not_approved():
    driver_mock = driver('Not')

    pto = PaidTimeOff(driver_mock)
    actual = pto.is_pto_day(datetime.now())

    assert actual is False
