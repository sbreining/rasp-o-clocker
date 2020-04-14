from src.config import Config
from .question import Question
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys


class Login:
    """A class to handle the responsibility of the login page for Paylocity.

    Attributes
    ----------
    _config : Config
        This holds onto the .env configuration

    _driver : WebDriver
        This is the instance of the web driver used to navigate.

    Methods
    -------
    login()
        Enter the credentials into the needed fields and login.
    """

    def __init__(self, config: Config, driver: WebDriver):
        """
        Creates a new instance of the PaidTimeOff page object.

        Parameters
        ----------
        config : Config
            The config object holding .env values for logging in.

        driver : WebDriver
            The chrome driver used to navigate around the browser.
        """
        self._config = config
        self._driver = driver

    def login(self) -> Question:
        """
        Locates text boxes for credentials and sends keys to login.

        Returns
        -------
        Question
            The Question page object in case we landed there.
        """
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
        return Question(self._config, self._driver)
