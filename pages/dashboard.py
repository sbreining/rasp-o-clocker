from . import pto


class Dashboard:
    def __init__(self, driver):
        self._driver = driver

    def clock_in(self):
        clock_in_element = self._driver.find_element_by_name('ClockIn')
        self._click_and_quit(clock_in_element)

    def start_lunch(self):
        start_lunch_element = self._driver.find_element_by_name('StartLunch')
        self._click_and_quit(start_lunch_element)

    def end_lunch(self):
        end_lunch_element = self._driver.find_element_by_name('EndLunch')
        self._click_and_quit(end_lunch_element)

    def clock_out(self):
        clock_out_element = self._driver.find_element_by_name('ClockOut')
        self._click_and_quit(clock_out_element)

    def go_to_pto(self):
        self._driver.find_element_by_name('SOME PTO IDENTIFIER').click()
        return pto.PaidTimeOff(self._driver)

    def _click_and_quit(self, element):
        element.click()
        self._driver.quit()
