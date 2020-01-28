# <div class="k-grid-content"> - Get elements from this guy
# Check the date RANGE of the bottom row, compare against today's date.
# Check if the status is 'Approved'
# Column 0 is date range, column 3 is approval status.

class PaidTimeOff:
    """A class that will handle find the PTO approvals.

    This page object will handle the intricacies of navigating to the PTO
    requests, then parsing the table, and validating if the given day is a
    requested PTO day that has been approved.

    Attributes
    ----------
    _driver : Webdriver
        The driver controlling the web browser.

    Methods
    -------
    is_pto_day()
        Navigates to the PTO page.
    """

    def __init__(self, driver):
        """
        Creates a new instance of the PaidTimeOff page object.

        Parameters
        ----------
        driver : WebDriver
            The chrome driver used to navigate around the browser.
        """
        self._driver = driver

    def is_pto_day(self, date):
        """
        Determines if `date` is the same day as a requested PTO day. It will
        return true if the date is an _approved_ PTO day.

        Parameters
        ----------
        date : datetime
            The date time object to test against PTO days.
        """
        self._driver.find_element_by_id('tabStatus').click()

        # BenefitsWidget
        parent = self._driver.find_element_by_id('BenefitsWidget')
        table = parent.find_element_by_class_name('k-grid-content')
        
        stuff = table.text.split('\n')

        row_of_importance = stuff.pop().split(' ')

        print('date %s is %s' % (row_of_importance[0], row_of_importance.pop()))

        is_pto = False

        # TODO Parse the table.

        # TODO Check the date month and day against the table of what is APPROVED

        # TODO Navigate back to the dashboard before returning.

        return is_pto
