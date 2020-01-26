from .dashboard import Dashboard
from selenium.webdriver.common.keys import Keys


class Question:
    """A class that will handle answering the secret question.

    This page object will handle all the intricacies of answering the secret
    question when presented.
    Future use will include checking the box to 'Remember this Computer' so
    that the secret question will be asked less frequently. This will leave
    less chance for error to occur in the process.

    Attributes
    ----------
    _config : Config
        Retrieves config values as necessary.

    _driver : Webdriver
        The driver controlling the web browser.

    Methods
    -------
    is_on_dashboard()
        Determines if it skipped the question page, and went straight to the
        dashboard.

    answer_question()
        Determines which question it is, and answers accordingly.
    """

    def __init__(self, config, driver):
        """
        Creates a new instance of the Question page object.

        Parameters
        ----------
        config : Config
            Configuration object that loaded the .env file.
        
        driver : WebDriver
            The chrome driver used to navigate around the browser.
        """
        self._config = config
        self._driver = driver

    def is_on_dashboard(self):
        """Returns true if the browser landed on the dashboard page."""
        return self._config.get_dashboard_url() in self._driver.current_url

    def answer_question(self):
        """Answers the secret question to continue to the Dashboard."""

        # Step 1: Figure out what the question is.
        secret_question = self._driver.find_element_by_xpath('//label[@for="ChallengeAnswer"]').text

        # Step 2: Enter text into box.
        answer_box = self._driver.find_element_by_id('ChallengeAnswer')
        answer_box.send_keys(self._config.get_questions()[secret_question])

        # Step 3: Hit enter to submit rather than finding the button.
        answer_box.send_keys(Keys.RETURN)
        
        return Dashboard(self._driver)