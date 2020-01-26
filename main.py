from config import Config
from selenium.webdriver import Chrome
from utility import Database, PagerDuty, PunchCardManager


def main():
    # Load up environment configuration
    config = Config()

    # Connect to the database
    db = Database(config)

    # Instantiate the driver
    driver = Chrome()
    driver.implicitly_wait(config.get_implicit_wait())

    # Instantiate the pager
    pager = PagerDuty(config)

    # Set the args in a dictionary for future use
    args = {'config': config, 'database': db, 'driver': driver, 'pager': pager}

    # Start the process manager
    punch_card_manager = PunchCardManager(args)
    punch_card_manager.start()


if __name__ == "__main__":
    main()
