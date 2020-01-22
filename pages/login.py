from . import question
from selenium.webdriver.common.keys import Keys


class Login:
    def __init__(self, config, driver):
        self._config = config
        self._driver = driver

    def login(self):
        payload = self._config.get_login()

        self._driver.get(self._config.get_login_url())

        # Insert the company ID for PayLease
        input_company_id = self._driver.find_element_by_id("CompanyId")
        input_company_id.send_keys(payload['companyId'])

        # Insert given username.
        input_username = self._driver.find_element_by_id("Username")
        input_username.send_keys(payload['username'])

        # Insert the super top secret password
        input_password = self._driver.find_element_by_id("Password")
        input_password.send_keys(payload['password'])

        # Just send return while still in the password field.
        # No need to actually click the submit button.
        input_password.send_keys(Keys.RETURN)

        # Nine times out of 10, we should be on the dashboard.
        return question.Question(self._config, self._driver)
