from datetime import datetime
from threading import Thread
import pages
import random
import time


class PunchCardManager(Thread):
    def __init__(self, group=None, target=None, name=None, args=None):
        super().__init__(group=group, target=target, name=name)

        self._config = args['config']
        self._driver = args['driver']
        self._db = args['database']

    def run(self):
        clock_out_hour = 0
        clock_out_minute = 0
        end_lunch = 0
        is_end_lunch_punched = True
        is_clock_out_punched = True
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

            if now.weekday() > 5 or \
               self._db.is_holiday(now.month, now.day) or \
               self._is_pto_day(dashboard_page, now):
                print('It is a weekend, holiday, or PTO day, skipping!')
                # TODO Uncomment when top level is loop: continue
            else:
                print('It is not a weekend, holiday, or PTO day.')

            if is_clock_out_punched and now.hour == 7:
                if 0 < now.minute <= 24:
                    # TODO Put these times in the database.
                    clock_out_hour = now.hour + 8
                    clock_out_minute = now.minute + random.randrange(33,35)
                    is_clock_out_punched = False
                    print('Clocking in for the day.')
                    dashboard_page.clock_in()
            elif is_end_lunch_punched and now.hour == 12:
                if 0 < now.minute <= 23:
                    end_lunch = now.minute + 31
                    is_end_lunch_punched = False
                    print('Starting lunch.')
                    dashboard_page.start_lunch()
            elif not is_end_lunch_punched and now.hour == 12:
                if now.minute > end_lunch:
                    is_end_lunch_punched = True
                    print('Lunch is over.')
                    dashboard_page.end_lunch()
            elif not is_clock_out_punched and now.hour > clock_out_hour:
                if now.minute > clock_out_minute:
                    is_clock_out_punched = True
                    print('Clocking out for the day.')
                    dashboard_page.clock_out()

            time.sleep(60)

    def _is_pto_day(self, dashboard, date):
        pto = dashboard.go_to_pto()

        return pto.is_pto_day(date)
