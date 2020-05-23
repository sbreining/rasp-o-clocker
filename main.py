from dotenv import load_dotenv
from os.path import join, dirname
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from smtplib import SMTP_SSL
from src.config import Config
from src.database import Database
from src.database.models import Holiday, Punch
from src.gui import MainWindow
from src.utility import PagerDuty, PunchCardManager, GMAIL_DOMAIN
from sys import exc_info
import tkinter as tk


def main() -> None:
    # Load up environment configuration
    load_dotenv(join(dirname(__file__), 'data', '.env'))
    config = Config()

    # Connect to the database
    db = Database(config)

    # Add the connection to the two models.
    holiday = Holiday(db)
    punch = Punch(db)

    # Set the options to have chrome be headless
    op = Options()
    op.add_argument('--headless')

    # Instantiate the driver
    driver = Chrome(options=op)
    driver.implicitly_wait(config.get_implicit_wait())

    # Instantiate the pager
    smtp = SMTP_SSL(GMAIL_DOMAIN)
    pager = PagerDuty(config, smtp)

    # Set the args in a dictionary for future use
    args = {
        'config': config,
        'driver': driver,
        'holiday': holiday,
        'pager': pager,
        'punch': punch
    }

    punch_card_manager = PunchCardManager(args)

    root = tk.Tk()
    app = MainWindow(master=root)
    app.mainloop()

    # TODO: Remove below this line, make it part of GUI.

    try:
        # Start the process manager
        punch_card_manager.start()
    except:
        exception_type, value = exc_info()[:2]
        pager.alert(
            'PROGRAM CRASH, needs restart.\nException - %s\nValue - %s' %
            (exception_type, value)
        )


if __name__ == "__main__":
    main()
