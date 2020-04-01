import sqlite3
from datetime import datetime
from calendar import month_name
from utility import Database


class Holiday:
    """A class that will handle Database interactions with the holidays table. 

    Attributes
    ----------
    _connection : Database
        A connection to the Database

    Methods
    -------
    add_holiday(date)
        Adds the holiday to the database.

    get_row_id_by_date(date)
        Returns the row ID for the given date passed in.

    is_holiday(date)
        Determines if the given date is a holiday.

    remove_holiday(date)
        Removes a holiday from the database.
    """

    def __init__(self, connection: Database):
        """
        Creates a new instance of the Holiday model object.

        Parameters
        ----------
        connection: Database, required
            The database connection.
        """
        self._connection = connection
    
    def add_holiday(self, date: datetime) -> int:
        """
        Adds a record to the database to create a holiday.

        Parameters
        -------
        date : datetime, required
            The date to add to the table.
        
        Return
        -------
        int
            On successful insert, returns row ID. On fail, return -1
        """
        sql = 'INSERT INTO holidays(month, day, year) VALUES(?, ?, ?)'
        data = (month_name[date.month], date.day, date.year,)

        try:
            self._connection.execute(sql, data)
            self._connection.commit()
        except sqlite3.OperationalError as exception:
            print(exception)
            return -1

        return self._connection.get_last_row_id()
    
    def get_row_id_by_date(self, date: datetime) -> int:
        """
        Finds the date in the database and returns the row ID.

        Parameters
        -------
        date : datetime, required
            The date time to be found in the database

        Return
        -------
        int
            The ID of the row for the holiday found, -1 on error or not found.
        """
        sql = 'SELECT id FROM holidays WHERE month=? AND day=? AND year=?'
        data = (month_name[date.month], date.day, date.year,)

        try:
            self._connection.execute(sql, data)
            row = self._connection.fetchall()[0]
        except sqlite3.OperationalError:
            return -1

        return row[0]

    def is_holiday(self, date: datetime) -> bool:
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

        try:
            self._connection.execute(sql, data)
            results = self._connection.fetchall()
        except sqlite3.OperationalError:
            # In this case we'll just consider it a holiday and not clock
            return True

        return len(results) != 0

    def remove_holiday(self, record_id: int) -> bool:
        """
        Removes the record belonging to the given ID that is passed in.

        Parameters
        -------
        record_id : int, required
            The ID of the row to be removed.
        
        Return
        -------
        bool
            True if the record deleted successfully.
        """
        sql = 'DELETE FROM holidays WHERE id=?'
        data = (record_id,)

        try:
            self._connection.execute(sql, data)
            self._connection.commit()
        except sqlite3.OperationalError:
            print('Could not delete record.')
            return False
        
        return True
