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

    write_holidays(holidays)
        Writes a list of holidays to the Database.
    """
    def __init__(self, config):
        self._db = sqlite3.connect(config.get_db_path(), check_same_thread=False)

    def is_holiday(self, month, day):
        """Checks if the day and month combination is a holiday.

        Parameters
        ----------
        month : str, required
            The name of the month to be checked, in string form.
        
        day : str, required
            The day of the month.
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

    def write_holidays(self, holidays):
        """Writes the holidays to the DB for the year.

        Parameters
        ----------
        holidays : array, required
            An array of tuples in the format; (month, day,)
        """
        cursor = self._db.cursor()

        # Remove all data from the table then;
        delete_sql = 'DELETE FROM holidays'
        cursor.execute(delete_sql)

        # Write all the new holidays retrieved from the PDF.
        insert_sql = 'INSERT INTO holidays(month, day) VALUES(?, ?);'
        cursor.executemany(insert_sql, holidays)

        # Commit changes to DB.
        self._db.commit()

        return
