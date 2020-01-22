from .dashboard import Dashboard


class Question:
    """A class that will handle answering the secret question. 

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
        self._config = config
        self._driver = driver

    def is_on_dashboard(self):
        """Returns true if the browser landed on the dashboard page."""
        return self._config.get_dashboard_url() in self._driver.current_url

    def answer_question(self):
        """Answers the secret question to continue to the Dashboard."""

        # Step 1: Figure out what the question is.
        secret_question = self._driver.find_element_by_id('some_id').text

        # Step 2: Enter text into box.
        answer_box = self._driver.find_element_by_id('answer_id')
        answer_box.send_keys(self._config.get_questions()[secret_question])

        # Step 3: Hit enter
        answer_box.send_keys(Keys.RETURN)
        
        return Dashboard(self._driver)
