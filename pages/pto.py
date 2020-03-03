from datetime import datetime
from datetime import timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
import time


DATE = 0
STATUS = 4
HOURS = 2


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
        driver : WebDriver, required
            The chrome driver used to navigate around the browser.
        """
        self._driver = driver

    def is_pto_day(self, date):
        """
        Determines if `date` is the same day as a requested PTO day. It will
        return true if the date is an _approved_ PTO day.

        Parameters
        ----------
        date : datetime, required
            The date time object to test against PTO days.

        Returns
        -------
        bool
            Returns True if the day is a PTO day, False otherwise.
        """
        self._driver.find_element_by_id('tabStatus').click()

        is_pto = self._determine_date_is_pto(self._get_pto_row(), date)

        self._navigate_back_to_dash()

        return is_pto

    @staticmethod
    def _determine_date_is_pto(nearest_pto, date):
        """
        This private function analyzes the row passed in to see if the given
        date is an approved PTO day.

        Parameters
        ----------
        nearest_pto : array, required
            Each column is split into a position in the array.

        date : datetime, required
            The date that is being compared against the range of requested days
            off.

        Returns
        -------
        bool
            Will return False if the day is not approved, or not in the range.
            It will return True otherwise.
        """
        # Early return if the PTO day is not approved.
        if nearest_pto[STATUS] != 'Approved':
            return False

        # Get the first day of the approved time off.
        first_date = datetime.strptime(nearest_pto[DATE], '%m/%d/%Y')

        # A day off is an 8 hour period. But it needs to be 0 based.
        days_approved = (int(nearest_pto[HOURS]) / 8) - 1
        end_day = first_date + timedelta(days=days_approved)

        return first_date <= date <= end_day

    def _get_pto_row(self):
        """
        Returns an array based on column of each value in the last row.

        Returns
        -------
        list
            A list of the row data from the paid time off page.
        """
        # Locate the div containing the approved PTO
        parent = self._driver.find_element_by_id('BenefitsWidget')

        # Get the table containing the rows of the time off.
        table = parent.find_element_by_class_name('k-grid-content')

        # Get the text out of the table, split on '\n' then get the last row.
        # The last row contains the closest date to that which is requested off.
        rows = table.text.split('\n')
        return rows.pop().split(' ')

    def _navigate_back_to_dash(self):
        """Returns back to the dashboard page."""
        self._driver.find_element_by_class_name('unav-main-menu-title').click()

        element = None
        try:
            element = WebDriverWait(self._driver, 1).until(
                ec.visibility_of_element_located(
                    (By.CLASS_NAME, 'unav-drawer-item-title')
                )
            )
        except TimeoutException:
            # Sleep for 3 extra seconds with hopes the menu opens up.
            time.sleep(3)
            element = self._driver.find_element_by_class_name(
                'unav-drawer-item-title'
            )
        finally:
            element.click()
