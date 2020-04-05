from os import getenv
from os.path import join, dirname


class Config:
    """A class that will handle loading up environment variables. 
    
    This class will load up the environment variables into the instantiated
    object, and read back environment values.

    Methods
    -------
    get_login()
        Returns login information including a company ID, login and password.

    get_login_url()
        Returns the url in string form for where to log in.

    get_dashboard_url()
        Returns the url for the dashboard page.

    get_implicit_wait()
        Returns the amount of time selenium should wait on the page to load.

    get_db_path()
        Returns path to the database, this relative to this file.

    get_questions()
        Returns the secret questions as key-value pairs in a python dictionary.
    
    get_pager_duty_info()
        Returns the information needed for PagerDuty
    
    get_start_hour()
        The hour to start the clock in process.
    """

    @staticmethod
    def get_login() -> dict:
        """
        Returns login information; company ID, login and password.

        Returns
        -------
        Dictionary
            Get login information using keys: companyId, username, and password.
        """
        return {
            'companyId': getenv('COMPANY_CODE'),
            'username': getenv('USERNAME'),
            'password': getenv('PASSWORD')
        }

    @staticmethod
    def get_login_url() -> str:
        """
        Returns the url in string form for where to log in.

        Returns
        -------
        string
        """
        return getenv('PAYLOCITY_LOGIN_URL')

    @staticmethod
    def get_dashboard_url() -> str:
        """
        Returns the url for the dashboard page.

        Returns
        -------
        string
        """
        return getenv('PAYLOCITY_BASE_URL')

    @staticmethod
    def get_implicit_wait() -> int:
        """
        Returns the max time (seconds) selenium waits for page load.

        Returns
        -------
        int
        """
        return int(getenv('IMPLICIT_WAIT'))

    @staticmethod
    def get_db_path() -> str:
        """
        Returns path to the database, this relative to this file.

        Returns
        -------
        string
        """
        return join(dirname(__file__), '../../data/database.db')

    @staticmethod
    def get_questions() -> dict:
        """
        Returns secret questions-answers as key-value pairs in dictionary.

        Returns
        -------
        Dictionary
            Use the secret questions as keys to get the secret answers.
        """
        return {
            getenv('SECRET_Q_1'): getenv('SECRET_A_1'),
            getenv('SECRET_Q_2'): getenv('SECRET_A_2'),
            getenv('SECRET_Q_3'): getenv('SECRET_A_3')
        }

    @staticmethod
    def get_pager_duty_info() -> dict:
        """
        Returns information necessary for PagerDuty

        Returns
        -------
        Dictionary
            Contains the information to login to the e-mail service for alerts.
        """
        return {
            'from': getenv('EMAIL_ADDRESS'),
            'password': getenv('EMAIL_PASSWORD'),
            'to': getenv('SMS_GATEWAY')
        }

    @staticmethod
    def get_start_hour() -> int:
        """
        Returns the hour at which to start work.

        Returns
        -------
        int
            The hour (based on 24 hour clock) to start work.
        """
        return int(getenv('STARTING_HOUR'))
