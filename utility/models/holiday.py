class Holiday:
    """A class that will handle Database interactions with the holidays table. 

    Attributes
    ----------
    _cursor : Cursor
        A connection to the Database

    Methods
    -------
    is_holiday(date)
        Determines if the given date is a holiday.
    """
    def __init__(self, cursor):
         """
        Creates a new instance of the Holiday model object.

        Parameters
        ----------
        cursor : Cursor, required
            A connection to the database.
        """
        self._cursor = cursor

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
        sql = 'SELECT * FROM holidays WHERE month=? AND day=? AND year=?;'
        data = (month_name[date.month], date.day, date.year,)
        self._cursor.execute(sql, data)

        data = cursor.fetchall()

        return len(data) != 0