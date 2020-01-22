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
    """
    def __init__(self):
        # Create .env file path.
        dotenv_path = join(dirname(__file__), '../.env')

        # Load file from the path.
        load_dotenv(dotenv_path)

    def get_login(self):
        """Returns login information; company ID, login and password."""
        return {
            'companyId': getenv('COMPANY_CODE'),
            'username': getenv('USERNAME'),
            'password': getenv('PASSWORD')
        }

    def get_login_url(self):
        """Returns the url in string form for where to log in."""
        return getenv('PAYLOCITY_LOGIN_URL')

    def get_dashboard_url(self):
        """Returns the url for the dashboard page."""
        return getenv('PAYLOCITY_BASE_URL')

    def get_implicit_wait(self):
        """Returns the max time (seconds) selenium waits for page load."""
        return getenv('IMPLICIT_WAIT')

    def get_db_path(self):
        """Returns path to the database, this relative to this file."""
        return join(dirname(__file__), '../data/database.db')
    
    def get_questions(self):
        """Returns secret questions-answers as key-value pairs in dictionary"""
        return {
            getenv('SECRET_Q_1'): getenv('SECRET_A_1'),
            getenv('SECRET_Q_2'): getenv('SECRET_A_2'),
            getenv('SECRET_Q_3'): getenv('SECRET_A_3')
        }
