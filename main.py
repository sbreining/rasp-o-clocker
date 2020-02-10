from config import Config
from dotenv import load_dotenv
from os.path import join, dirname
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from sys import exc_info
from utility import Database, PagerDuty, PunchCardManager


def main():
    # Load up environment configuration
    load_dotenv(join(dirname(__file__), './.env'))
    config = Config()

    # Connect to the database
    db = Database(config)

    # Set the options to have chrome be headless
    op = Options()
    op.add_argument('--headless')

    # Instantiate the driver
    driver = Chrome(options=op)
    driver.implicitly_wait(config.get_implicit_wait())

    # Instantiate the pager
    pager = PagerDuty(config)

    # Set the args in a dictionary for future use
    args = {'config': config, 'database': db, 'driver': driver, 'pager': pager}

    # Start the process manager
    punch_card_manager = PunchCardManager(args)

    try:
        punch_card_manager.start()
    except:
        exception_type, value = exc_info()[:2]
        pager.alert('PROGRAM CRASH, needs restart.\nException - %s\nValue - %s' % (exception_type, value))


if __name__ == "__main__":
    main()
