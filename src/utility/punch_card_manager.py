from datetime import date, datetime, timedelta
from src.pages import Dashboard, Login
from random import randint
from selenium.common.exceptions import NoSuchElementException
from src.database.models import Holiday, Punch
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

    login_to_paylocity()
        Handles the actions of logging into paylocity.

    is_clock_in_day(now, dashboard_page)
        Returns true if punches are supposed to occur for the day.

    check_resources(now)
        This checks day of week, holiday table, and PTO table.

    perform_action(action, action_str, time_of_action, db_action)
        Performs the punch action based on the time of day.

    get_punch(punch_id, position)
        Gets the column from the punches table to compare datetimes.
    """

    def __init__(self, args: dict):
        """
        Instantiates the punch card manager instance.

        Parameters
        ----------
        args : dictionary, required
            Holds all necessary objects to make this manager function.
        """
        self._config = args['config']
        self._driver = args['driver']
        self._holiday = args['holiday']
        self._pager = args['pager']
        self._punch = args['punch']

        self._start_hour = self._config.get_start_hour()

    def start(self) -> None:
        """This function runs the show, making everything mesh together."""
        if self._punch.get_most_recent_day() is None:
            self._punch.insert_new_day()

        while True:
            punch_card = self._punch.get_most_recent_day()

            date_str = '%s 00:00:00.000' % punch_card[1]
            cur_punch_day = self.get_datetime_from_date_string(date_str).date()

            if date.today() - cur_punch_day >= timedelta(days=1):
                self._punch.insert_new_day()

            now = datetime.now()

            if not self.is_clock_in_day(now):
                # If it is not a day to clock in, sleep for greater intervals.
                time.sleep(300)
                continue

            if punch_card[3] is None and now.hour == self._start_hour:
                self.perform_action('Clock In', now, self._punch.in_)
            elif self.should_punch(punch_card, 3, 4, now, timedelta(hours=4, minutes=randint(1, 30))):
                self.perform_action('Start Lunch', now, self._punch.start)
            elif self.should_punch(punch_card, 4, 5, now, timedelta(minutes=randint(31, 35))):
                self.perform_action('End Lunch', now, self._punch.end)
            elif self.should_punch(punch_card, 3, 6, now, timedelta(hours=8, minutes=randint(40, 45))):
                self.perform_action('Clock Out', now, self._punch.out)

            time.sleep(60)

    def login_to_paylocity(self) -> Dashboard:
        """
        This function logs into Paylocity and bypasses the secret question
        page if that pops up.

        Returns
        -------
        Dashboard
            The Dashboard page object.
        """
        # The sequence of steps below is contingent on the time.
        login_page = Login(self._config, self._driver)
        question_page = login_page.login()

        # The login might've gone straight to the dashboard
        if not question_page.is_on_question_page():
            return Dashboard(self._driver)

        return question_page.answer_question()

    def is_clock_in_day(self, now: datetime) -> bool:
        """
        This function determines whether today is a day to clock in or not. It
        will do so by checking if it is a weekend, company holiday, or a
        requested and approved day off.

        Parameters
        ----------
        now : datetime, required
            The date to check against.

        Returns
        -------
        bool
            Will return true for a day to clock in, false otherwise.
        """
        determined = self._punch.is_work_day()
        if determined is not None:
            return determined

        is_clock_day = self.check_resources(now)

        self._punch.update_is_work_day(is_clock_day)

        return is_clock_day

    def check_resources(self, now: datetime) -> bool:
        """
        This method validates against the various resources if this is an
        appropriate day to clock in or not. It starts with the day of the week
        and holidays as they are the quickest checks. Then, if those do not
        apply, logs into Paylocity and checks the PTO charts. This will later
        be saved so this function is only run once a day.

        Parameters
        ----------
        now : datetime, required
            The day to check against, if the hours are included, no big deal.

        Returns
        -------
        bool
            False on a day which is not supposed to clock in and out, True
            otherwise.
        """
        if now.weekday() > 5 or self._holiday.is_holiday(now):
            print('It is a weekend or holiday, skipping!')
            return False

        # If it is not holiday or weekend, check PTO.
        dashboard_page = self.login_to_paylocity()
        return not dashboard_page.go_to_pto().is_pto_day(now)

    def perform_action(self, action_str: str, time_of_action: datetime, db_action: callable) -> None:
        """
        This function handles the action and error handling for each punch
        for the day. It will alert if anything is at critical. Currently, even
        INFO level messages will be sent to PagerDuty. Later, a .env var will
        be included to set level of pages.

        Parameters
        ----------
        action_str : string, required
            The name of the action being performed.

        time_of_action : datetime, required
            The time at which the action is occurring.

        db_action : callback, required
            The action of logging in the database.
        """
        dashboard = self.login_to_paylocity()
        action = {
            'Clock In': dashboard.clock_in,
            'Start Lunch': dashboard.start_lunch,
            'End Lunch': dashboard.end_lunch,
            'Clock Out': dashboard.clock_out
        }
        try:
            action[action_str]()
            self._pager.info(
                '%s at %s' % (action_str, time_of_action.strftime('%c'))
            )
        except NoSuchElementException:
            self._pager.alert('Did not %s successfully.' % action_str)

        if not db_action(time_of_action):
            self._pager.warning('Did not log %s to database' % action_str)

    def should_punch(self, punch_card: tuple, prev_punch_pos: int, cur_punch_pos: int, now: datetime, delta: timedelta) -> bool:
        """
        This function takes the ID of the punch, and the position desired for
        clocking in and out.

        Parameters
        ----------
        punch_card : tuple, required
            This is the collection from the database.

        prev_punch_pos : int, required
            The position of the column desired to compare against.

        cur_punch_pos : int, required
            Check to make sure the punch is None so we don't over punch it.

        now : datetime, required
            Going to ensure we pass the timedelta.

        delta : timedelta, required
            The delta to cover.

        Returns
        -------
        bool
            Returns if we should perform the action or not.
        """
        if punch_card[cur_punch_pos] is not None:
            return False

        last_punch_str = punch_card[prev_punch_pos]
        if last_punch_str is None:
            return False

        last_punch = self.get_datetime_from_date_string(last_punch_str)

        return now - last_punch > delta

    @staticmethod
    def get_datetime_from_date_string(date_str: str) -> datetime:
        """
        Converts a string from given format into a datetime object.

        Examples
        --------
        2020-01-01 01:01:01.010101
        1923-06-12 15:42:59.326458

        Parameters
        ----------
        date_str : string, required
            The string that will be parsed and turned into a datetime.

        Returns
        -------
        datetime
            The datetime object that was parsed from the string passed in.
        """
        return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f')
