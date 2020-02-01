from config import Config
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from sys import exc_info
from utility import Database, PagerDuty, PunchCardManager


def main():
    # Load up environment configuration
    config = Config()

    # Connect to the database
    db = Database(config)

    # Set the options to have chrome be headless
    c_op = Options()
    c_op.add_argument('--headless')

    # Instantiate the driver
    driver = Chrome(chrome_options=c_op)
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
        exctype, value = exc_info()[:2]
        pager.alert('PROGRAM CRASH, needs restart.\nException - %s\nValue - %s' % (exctype, value))


if __name__ == "__main__":
    main()
