from .pto import PaidTimeOff


class Dashboard:
    """Handle interactions with the landing dashboard on Paylocity.

    Attributes
    ----------
    _driver : WebDriver
        This is the instance of the web driver used to navigate.

    Methods
    -------
    clock_in()
        Find the button for clocking in and click it.

    start_lunch()
        Find the button for starting lunch and click it.

    end_lunch()
        Find the button for ending lunch and click it.

    clock_out()
        Find the button for clocking out and click it.

    go_to_pto()
        Navigate to the page containing PTO.

    _click_and_nav_away(element)
        Click on the provided element, and navigate to www.google.com
    """

    def __init__(self, driver):
        """
        Creates a new instance of the Dashboard page object.

        Parameters
        ----------
        driver : WebDriver
            The chrome driver used to navigate around the browser.
        """
        self._driver = driver

    def clock_in(self):
        """Finds the element to clock in, and sends to _click_and_nav."""
        clock_in_element = self._driver.find_element_by_name('ClockIn')
        self._click_and_nav_away(clock_in_element)

    def start_lunch(self):
        """Finds the element to start lunch, and sends to _click_and_nav."""
        start_lunch_element = self._driver.find_element_by_name('StartLunch')
        self._click_and_nav_away(start_lunch_element)

    def end_lunch(self):
        """Finds the element to end lunch, and sends to _click_and_nav."""
        end_lunch_element = self._driver.find_element_by_name('EndLunch')
        self._click_and_nav_away(end_lunch_element)

    def clock_out(self):
        """Finds the element to clock out, and sends to _click_and_nav."""
        clock_out_element = self._driver.find_element_by_name('ClockOut')
        self._click_and_nav_away(clock_out_element)

    def go_to_pto(self):
        """
        Will navigate to the page with the table of PTO approvals.

        Return
        -------
        PaidTimeOff
            The PTO page object to handle finding PTO.
        """
        self._driver.find_element_by_xpath('//a[text()="Launch Time & Attendance"]').click()
        return PaidTimeOff(self._driver)

    def _click_and_nav_away(self, element):
        """Clicks on provided element and navigates away from Paylocity.

        The only reason to navigate away from Paylocity is to simulate logging
        out of the service. It is unnecessary to close and re-open the web
        browser regularly. Further, it does not make sense to stay on the
        Paylocity web page, just to have it log use out due to expired session.

        Parameters
        -------
        element : WebElement, required
            The web element that should be clicked on.
        """
        element.click()
        self._driver.get('www.google.com')
