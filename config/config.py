from os import getenv
from os.path import join, dirname
from dotenv import load_dotenv


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
    """
    def __init__(self):
        # Create .env file path.
        dotenv_path = join(dirname(__file__), '../.env')

        # Load file from the path.
        load_dotenv(dotenv_path)

    def get_login(self):
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

    def get_login_url(self):
        """
        Returns the url in string form for where to log in.

        Returns
        -------
        string
        """
        return getenv('PAYLOCITY_LOGIN_URL')

    def get_dashboard_url(self):
        """
        Returns the url for the dashboard page.

        Returns
        -------
        string
        """
        return getenv('PAYLOCITY_BASE_URL')

    def get_implicit_wait(self):
        """
        Returns the max time (seconds) selenium waits for page load.

        Returns
        -------
        int
        """
        return getenv('IMPLICIT_WAIT')

    def get_db_path(self):
        """
        Returns path to the database, this relative to this file.

        Returns
        -------
        string
        """
        return join(dirname(__file__), '../data/database.db')
    
    def get_questions(self):
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
    
    def get_pager_duty_info(self):
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
    
    def get_start_hour(self):
        """
        Returns the hour at which to start work.

        Returns
        -------
        int
            The hour (based on 24 hour clock) to start work.
        """
        return int(getenv('STARTING_HOUR'))
