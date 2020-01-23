import sqlite3
from calendar import month_name


class Database:
    """A class that will handle Database interactions. 
    
    The connection to the database will be managed by this class object. No ORM
    will be used as there are very few interactions.

    Attributes
    ----------
    _db : Connection
        A connection to the Database

    Methods
    -------
    get_cursor()
        Returns the cursor with the connection to the database.
    """

    def __init__(self, config):
        """
        Creates a new instance of the Database object.

        Parameters
        ----------
        config : Config
            Configuration object that loaded the .env file.
        """
        self._db = sqlite3.connect(config.get_db_path(), check_same_thread=False)
        self.cursor = self._db.cursor()
    
    def get_cursor():
        return self.cursor
