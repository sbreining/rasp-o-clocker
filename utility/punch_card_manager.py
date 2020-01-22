from datetime import datetime
from threading import Thread
import pages


class PunchCardManager(Thread):
    def __init__(self, group=None, target=None, name=None, args=None):
        super().__init__(group=group, target=target, name=name)

        self._config = args['config']
        self._driver = args['driver']
        self._db = args['database']

    def run(self):
        # TODO Make this a while loop to keep it running
        if True:
            # TODO Handle the times at which I need to log in.
            # TODO breaks will likely be continues at some point?
            # TODO Will storing start time and start lunch in DB be better.
            #   Restarts will not detract from that. And we can do some date math.

            # The sequence of steps below is contingent on the time.
            login_page = pages.login.Login(self._config, self._driver)
            question_page = login_page.login()

            # The login might've gone straight to the dashboard
            if question_page.is_on_dashboard():
                dashboard_page = pages.dashboard.Dashboard(self._driver)
                print('We are on the dashboard')
            else:
                dashboard_page = question_page.answer_question()
                print('The question page happened')

            now = datetime.now()

            if now.weekday() > 5 or self._db.is_holiday(now.month, now.day):
                print('It is a weekend or Holiday, skipping!')
                break
            else:
                print('It is not a weekend or holiday.')

            punch_command = ''
            if now.hour == 8:
                if 0 < now.minute <= 30:
                    punch_command = 'in'
            elif now.hour == 12:
                if 0 < now.minute <= 30:
                    punch_command = 'sl'  # Start Lunch
                    # Need to figure out how to do lunch 31-35 minutes later.

            # TODO Uncomment this: break
