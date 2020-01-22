class PaidTimeOff:
    # <a id="tabStatus">Status</a> Click to get approval days off
    # <div class="k-grid-content"> - Get elements from this guy
    # Check the date RANGE of the bottom row, compare against today's date.
    # Check if the status is 'Approved'
    # Column 0 is date range, column 3 is approval status.
    def __init__(self, driver):
        self._driver = driver
