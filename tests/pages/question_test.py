from pages import Dashboard
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from unittest.mock import call, Mock
import pytest


# Unit under test
from pages import Question


question_text = 'test question'
answer_text = 'test answer'


@pytest.fixture()
def config():
    questions = {question_text: answer_text}

    config = Mock()
    config.get_questions = Mock(return_value=questions)

    return config


@pytest.fixture()
def driver():
    driver = Mock()

    question_element = Mock(text=question_text)
    driver.find_element_by_xpath = Mock(return_value=question_element)

    return driver


def test_is_on_question_page_returns_false(config, driver):
    driver.find_element_by_class_name = Mock()

    question_page = Question(config, driver)
    actual = question_page.is_on_question_page()

    driver.find_element_by_class_name.assert_called_once_with('header-nav')
    assert actual is False


def test_is_on_question_page_throws_and_returns_true(config, driver):
    driver.find_element_by_class_name = Mock(side_effect=NoSuchElementException())

    question_page = Question(config, driver)
    actual = question_page.is_on_question_page()

    driver.find_element_by_class_name.assert_called_once_with('header-nav')
    assert actual is True


def test_answer_question(config, driver):
    question_element = Mock()
    question_element.send_keys = Mock()

    driver.find_element_by_id = Mock(return_value=question_element)

    question_page = Question(config, driver)
    dash_page = question_page.answer_question()

    driver.find_element_by_xpath.assert_called_once_with('//label[@for="ChallengeAnswer"]')
    driver.find_element_by_id.assert_called_once_with('ChallengeAnswer')
    question_element.send_keys.assert_has_calls([call(answer_text), call(Keys.RETURN)])
    assert isinstance(dash_page, Dashboard)
