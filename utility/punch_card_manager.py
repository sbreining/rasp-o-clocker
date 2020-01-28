from datetime import datetime, timedelta
from utility.models import *
from random import randint
from selenium.common.exceptions import NoSuchElementException
import pages
import time


class PunchCardManager:
    """This class is the general manager of the system.

    It will handle validation, logging, and punching.

    Attributes
    ----------
    _config : Config
        Holds onto the configuration of the system.

    _driver : Webdriver
        The webdriver that controls the actions.

    _holiday : Holiday
        Model controlling the interactions with the holidays table.

    _pager : PagerDuty
        Responsible for notifying user of actions taken.

    _punch : Punch
        Model controlling the interactions with the punches table.

    _start_hour : int
        The hour which each day will start, not variable.

    Methods
    -------
    start()
        Starts the system working.

    _get_punch(punch_id, position)
        Gets the column from the punches table to compare datetimes.

    _is_clock_in_day(now, dashboard_page)
        Returns true if punches are supposed to occur for the day.

    _login_to_paylocity()
        Handles the actions of logging into paylocity.

    _perform_action(action, action_str, time_of_action, db_action)
        Performs the punch action based on the time of day.
    """
    def __init__(self, args):
        """
        Instantiates the punch card manager instance.

        Parameters
        ----------
        args : dictionary, required
            Holds all necessary objects to make this manager function.
        """
        self._config = args['config']
        self._driver = args['driver']
        self._pager = args['pager']

        self._start_hour = self._config.get_start_hour()
        self._holiday = Holiday(args['database'])
        self._punch = Punch(args['database'])

    def start(self):
        """This function runs the show, making everything mesh together."""
        while True:
            dashboard_page = self._login_to_paylocity()

            now = datetime.now()

            if not self._is_clock_in_day(now, dashboard_page):
                # If it is not a day to clock in, sleep for greater intervals.
                time.sleep(300)
                continue

            punch_id = self._punch.get_id()
            if punch_id == 0 and now.hour == self._start_hour:
                self._perform_action(dashboard_page.clock_in, 'Clock In', now, self._punch.in_)
            elif now - self._get_punch(punch_id, 1) > timedelta(hours=4, minutes=randint(1, 30)):
                self._perform_action(dashboard_page.start_lunch, 'Start Lunch', now, self._punch.start)
            elif now - self._get_punch(punch_id, 2) > timedelta(minutes=randint(31, 35)):
                self._perform_action(dashboard_page.end_lunch, 'End Lunch', now, self._punch.end)
            elif now - self._get_punch(punch_id, 3) > timedelta(hours=4, minutes=randint(5, 10)):
                self._perform_action(dashboard_page.clock_out, 'Clock Out', now, self._punch.out)

            time.sleep(60)

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
        if not question_page.is_on_question_page():
            return pages.Dashboard(self._driver)

        return question_page.answer_question()

    def _is_clock_in_day(self, now, dashboard_page):
        """
        This function determines whether today is a day to clock in or not. It
        will do so by checking if it is a weekend, company holiday, or a
        requested and approved day off.

        Parameters
        ----------
        now : datetime, required
            The date to check against.

        dashboard_page : Dashboard, required
            Used for navigation to the PTO page.

        Returns
        -------
        bool
            Will return true for a day to clock in, false otherwise.
        """
        if now.weekday() > 5 or self._holiday.is_holiday(now) or dashboard_page.go_to_pto().is_pto_day(date):
            print('It is a weekend, holiday, or PTO day, skipping!')
            return False

        print('It is not a weekend, holiday, or PTO day.')
        return True

    def _perform_action(self, action, action_str, time_of_action, db_action):
        """
        This function handles the action and error handling for each punch
        for the day. It will alert if anything is at critical. Currently, even
        INFO level messages will be sent to PagerDuty. Later, a .env var will
        be included to set level of pages.

        Parameters
        ----------
        action : callback, required
            The action to be performed on Paylocity's dashboard.

        action_str : string, required
            The name of the action being performed.

        time_of_action : datetime, required
            The time at which the action is occurring.

        db_action : callback, required
            The action of logging in the database.
        """
        try:
            action()
            self._pager.info('%s at %s' % (action_str, time_of_action.strftime('%c')))
        except NoSuchElementException:
            self._pager.alert('Did not %s successfully.' % (action_str))

        if not db_action(time_of_action):
            self._pager.warning('Did not log %s to database' % (action_str))

    def _get_punch(self, punch_id, position):
        """
        This function takes the ID of the punch, and the position desired for
        clocking in and out.

        Parameters
        ----------
        punch_id : int, required
            The ID of the row for the punches for the day.

        position : int, required
            The position of the column desired to compare against.

        Returns
        -------
        datetime
            Converts the string in the database into a datetime object.
        """
        return datetime.strptime(self._punch.get_punch_by_id(punch_id)[position], '%Y-%m-%d %H:%M:%S.%f')
