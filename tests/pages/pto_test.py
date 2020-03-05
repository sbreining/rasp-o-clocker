from datetime import datetime, timedelta
from pages import PaidTimeOff
from unittest.mock import Mock, patch
from selenium.common.exceptions import TimeoutException


clickable_element = Mock()
clickable_element.click = Mock()


def driver(start_date='01/01/01', hours='8', status='Approved'):
    table = Mock(text='%s x %s x %s x' % (start_date, hours, status))

    parent_element = Mock()
    parent_element.click = Mock()
    parent_element.find_element_by_class_name = Mock(return_value=table)

    nav_bar_element = Mock()
    nav_bar_element.click = Mock()

    driver_mock = Mock()
    driver_mock.find_element_by_id = Mock(return_value=parent_element)
    driver_mock.find_element_by_class_name = Mock(return_value=nav_bar_element)

    return driver_mock


@patch('selenium.webdriver.support.ui.WebDriverWait.until')
def test_is_pto_day_returns_false_when_request_not_approved(mock_until):
    driver_mock = driver(status='Not')
    mock_until = Mock(return_value=clickable_element)

    pto = PaidTimeOff(driver_mock)
    actual = pto.is_pto_day(datetime.now())

    assert actual is False


@patch('time.sleep')
def test_navigate_back_to_dash_throws_timeout(mock_sleep):
    driver_mock = driver(status='Does not matter in this test')
    mock_sleep = Mock()

    pto = PaidTimeOff(driver_mock)
    actual = pto.is_pto_day(datetime.now())

    assert actual is False


@patch('selenium.webdriver.support.ui.WebDriverWait.until')
def test_is_pto_day_returns_false_when_today_is_after(mock_until):
    mock_until = Mock(return_value=clickable_element)

    start_date = (datetime.now() + timedelta(days=-3)).strftime('%m/%d/%Y')
    mock_driver = driver(start_date=start_date, hours='16')

    pto = PaidTimeOff(mock_driver)
    actual = pto.is_pto_day(datetime.now())

    assert actual is False


@patch('selenium.webdriver.support.ui.WebDriverWait.until')
def test_is_pto_day_returns_false_when_today_is_prior(mock_until):
    mock_until = Mock(return_value=clickable_element)

    start_date = (datetime.now() + timedelta(days=1)).strftime('%m/%d/%Y')
    mock_driver = driver(start_date=start_date, hours='16')

    pto = PaidTimeOff(mock_driver)
    actual = pto.is_pto_day(datetime.now())

    assert actual is False


@patch('selenium.webdriver.support.ui.WebDriverWait.until')
def test_is_pto_day_returns_true_when_today_is_in_bounds(mock_until):
    mock_until = Mock(return_value=clickable_element)

    start_date = (datetime.now() + timedelta(days=-1)).strftime('%m/%d/%Y')
    mock_driver = driver(start_date=start_date, hours='24')

    pto = PaidTimeOff(mock_driver)
    actual = pto.is_pto_day(datetime.now())

    assert actual is True