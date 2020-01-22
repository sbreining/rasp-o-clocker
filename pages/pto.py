class PaidTimeOff:
    # <div class="k-grid-content"> - Get elements from this guy
    # Check the date RANGE of the bottom row, compare against today's date.
    # Check if the status is 'Approved'
    # Column 0 is date range, column 3 is approval status.
    def __init__(self, driver):
        self._driver = driver

    def is_pto_day(self, date):
        self._driver.find_element_by_id('tabStatus').click()

        # TODO Parse the table for python to understand.

        # TODO Check the date month and day against the table of what is APPROVED

        return True
