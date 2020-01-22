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
    is_holiday(month, day)
        Checks if the provided month and day is a holiday.
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

    def is_holiday(self, month, day):
        """
        Checks if the day and month combination is a holiday.

        Parameters
        ----------
        month : str, required
            The name of the month to be checked, in string form.
        
        day : str, required
            The day of the month.

        Return
        ----------
        bool
            True if day is a holiday.
        """
        print('Checking if holiday')
        cursor = self._db.cursor()

        # Set query statement
        cursor.execute(
            'SELECT * FROM holidays WHERE month=? AND day=?;',
            (month_name[month], day,)
        )
        data = cursor.fetchall()

        return len(data) != 0
