from datetime import datetime
from utility.models import *
import pages
import time


class PunchCardManager:
    def __init__(self, args):
        self._config = args['config']
        self._driver = args['driver']
        self._pager = args['pager']

        self._holiday = Holiday(args['database'])
        self._punch = Punch(args['database'])

    def start(self):
        while True:
            dashboard_page = self._login_to_paylocity()

            now = datetime.now()

            if not self._is_clock_in_day(now, dashboard_page):
                continue

            # TODO Need to utilize database.
            if self._punch.get_id() == 0 and now.hour == 7 and 0 < now.minute <= 24:
                self._clock_in(dashboard_page, now)
            elif now.hour == 12 and 0 < now.minute <= 23:
                self._start_lunch(dashboard_page, now)
            elif now.hour == 12 and now.minute >= 54:
                self._end_lunch(dashboard_page, now)
            elif now.hour == 15 and now.minute >= 30:
                self._clock_out(dashboard_page, now)


            time.sleep(60)

    def _is_pto_day(self, dashboard, date):
        pto = dashboard.go_to_pto()

        return pto.is_pto_day(date)

    def _login_to_paylocity(self):
        """
        This function logs into Paylocity and bypasses the secret question
        page if that pops up.

        Returns
        -------
        Dashboard
            The Dashboard page object.
        """
        # The sequence of steps below is contingent on the time.
        login_page = pages.Login(self._config, self._driver)
        question_page = login_page.login()

        # The login might've gone straight to the dashboard
        if question_page.is_on_dashboard():
            dashboard_page = pages.Dashboard(self._driver)
            print('We are on the dashboard')
        else:
            dashboard_page = question_page.answer_question()
            print('The question page happened')

        return dashboard_page

    def _is_clock_in_day(self, now, dashboard_page):
        if now.weekday() > 5 or \
                self._holiday.is_holiday(now) or \
                self._is_pto_day(dashboard_page, now):
            print('It is a weekend, holiday, or PTO day, skipping!')
            return False

        print('It is not a weekend, holiday, or PTO day.')
        return True

    # TODO The 4 functions below this are really repetitive. Fix that.
    def _clock_in(self, dashboard_page, now):
        try:
            dashboard_page.clock_in()
            self._punch.in_(now)
            self._pager.info('Clocked in at ' + now.isoformat())
        except:
            self._pager.alert('Did not clock in successfully.')

    def _start_lunch(self, dashboard_page, now):
        try:
            dashboard_page.start_lunch()
            self._punch.start(now)
            self._pager.info('Started lunch at ' + now.isoformat())
        except:
            self._pager.alert('Did not start lunch successfully.')

    def _end_lunch(self, dashboard_page, now):
        try:
            dashboard_page.end_lunch()
            self._punch.end(now)
            self._pager.info('Ended lunch at ' + now.isoformat())
        except:
            self._pager.alert('Did not end lunch successfully.')

    def _clock_out(self, dashboard_page, now):
        try:
            dashboard_page.clock_out()
            self._punch.out(now)
            self._pager.info('Clocked out at ' + now.isoformat())
        except:
            self._pager.alert('Did not clock out successfully.')
