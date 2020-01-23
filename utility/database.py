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

    def is_holiday(self, date):
        """
        Checks if the month-day-year combination is a holiday.

        Parameters
        ----------
        date : datetime, required
            The date to check against the database to see if it is a holiday.

        Return
        ----------
        bool
            True if day is a holiday.
        """
        cursor = self._db.cursor()

        sql = 'SELECT * FROM holidays WHERE month=? AND day=? AND year=?;'
        data = (month_name[date.month], date.day, date.year,)
        cursor.execute(sql, data)

        data = cursor.fetchall()

        return len(data) != 0
