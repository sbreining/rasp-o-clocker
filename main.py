from config.config import Config
from selenium.webdriver import Chrome
from utility.punch_card_manager import PunchCardManager
from utility.database import Database


def main():
    # Load up environment configuration
    config = Config()

    # Connect to the database
    db = Database(config)

    # Instantiate the driver
    driver = Chrome()
    driver.implicitly_wait(config.get_implicit_wait())

    # Set the args and driver in a dictionary for future use
    args = {'config': config, 'driver': driver, 'database': db}

    # Start the process manager
    punch_card_manager = PunchCardManager(args=args)
    punch_card_manager.start()


if __name__ == "__main__":
    main()
