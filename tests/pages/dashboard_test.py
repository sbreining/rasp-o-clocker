from src.pages import PaidTimeOff
from unittest.mock import Mock
import pytest


# Unit under test
from src.pages import Dashboard


def test_init_returns_instance_of_dashboard():
    dashboard = Dashboard(Mock())

    assert isinstance(dashboard, Dashboard)


@pytest.fixture()
def dash_and_action():
    mock_element = Mock()
    mock_element.click = Mock()

    driver = Mock()
    driver.get = Mock()
    driver.find_element_by_name = Mock(return_value=mock_element)

    dash = Dashboard(driver)

    return dash, mock_element, driver


def test_clock_in_calls_click_and_nav_away(dash_and_action):
    dash, action, driver = dash_and_action
    dash.clock_in()

    _run_action_assertions(action, driver)


def test_start_lunch_calls_click_and_nav_away(dash_and_action):
    dash, action, driver = dash_and_action
    dash.start_lunch()

    _run_action_assertions(action, driver)


def test_end_lunch_calls_click_and_nav_away(dash_and_action):
    dash, action, driver = dash_and_action
    dash.end_lunch()

    _run_action_assertions(action, driver)


def test_clock_out_calls_click_and_nav_away(dash_and_action):
    dash, action, driver = dash_and_action
    dash.clock_out()

    _run_action_assertions(action, driver)


def test_go_to_pto_clicks_element_and_returns_page_object():
    mock_element = Mock()
    mock_element.click = Mock()

    driver = Mock()
    driver.get = Mock()
    driver.find_element_by_xpath = Mock(return_value=mock_element)

    dash = Dashboard(driver)
    page = dash.go_to_pto()

    driver.find_element_by_xpath.assert_called_once_with('//a[text()="Launch Time & Attendance"]')
    mock_element.click.assert_called_once()
    assert isinstance(page, PaidTimeOff)


def _run_action_assertions(action, driver):
    driver.find_element_by_name.assert_called_once()
    action.click.assert_called_once()
    driver.get.assert_called_once()
