from src.pages import Question
from unittest.mock import call, Mock
from selenium.webdriver.common.keys import Keys


# Unit under test
from src.pages import Login


company_id = "12345"
username = "username"
password = "password"

company_id_element = Mock()
company_id_element.send_keys = Mock()

username_element = Mock()
username_element.send_keys = Mock()

password_element = Mock()
password_element.send_keys = Mock()

elements = {
    "CompanyId": company_id_element,
    "Username": username_element,
    "Password": password_element
}


def mock_find_element_by_id(arg):
    return elements[arg]


def test_login_sends_credentials_and_returns_question():
    login_creds = {
        "companyId": company_id,
        "username": username,
        "password": password
    }
    fake_url = 'some_url_here.com'

    config = Mock()
    config.get_login = Mock(return_value=login_creds)
    config.get_login_url = Mock(return_value=fake_url)

    driver = Mock()
    driver.get = Mock()
    driver.find_element_by_id = mock_find_element_by_id

    login_page = Login(config, driver)

    question_page = login_page.login()

    config.get_login.assert_called_once()
    config.get_login_url.assert_called_once()
    driver.get.assert_called_once_with(fake_url)
    company_id_element.send_keys.assert_called_once_with(company_id)
    username_element.send_keys.assert_called_once_with(username)
    password_element.send_keys.assert_has_calls([call(password), call(Keys.RETURN)])
    assert isinstance(question_page, Question)
