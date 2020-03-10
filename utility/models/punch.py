from utility import Database
from datetime import date, datetime
import sqlite3


class Punch:
    """A class that will handle Database interactions with the holidays table. 

    Attributes
    ----------
    _connection : Database
        A connection to the Database.

    Methods
    -------
    get_punch_by_id(id_)
        Get the punch by the ID of the row.

    in_(datetime)
        Inserts the row, and updates the clock in time.

    start(datetime)
        Updates the punch card to have the time lunch started.

    end(datetime)
        Updates the punch card to have the time lunch ended.

    out(datetime)
        Updates the punch card to have the time the day ended.

    insert_new_day()
        Adds a new day to the table for tracking punches.

    get_most_recent_day()
        Will return the most recent day added to the table.

    is_work_day()
        Using last row inserted, this will return bool determining if work day.

    update_is_work_day(is_work_day)
        Updates the punch day to determine if punches are needed or not.

    _update_punch(datetime, sql)
        This private method handles updating the punches for the day.
    """

    def __init__(self, connection: Database):
        """
        Creates a new instance of the Punch model object.

        Parameters
        ----------
        connection : Database, required
            Holds on to database connection.
        """
        self._connection = connection

    def get_punch_by_id(self, id_: int) -> tuple:
        """
        Retrieves the punch row by the id.

        Parameters
        ----------
        id_ : int, required
            The ID of the row to retrieve.

        Returns
        -------
        tuple
            The row, an empty tuple on failure.
        """
        sql = 'SELECT * FROM punches WHERE id=?'
        data = (id_,)

        try:
            self._connection.execute(sql, data)
        except sqlite3.OperationalError:
            return ()

        return self._connection.fetchone()

    def in_(self, datetime_obj: datetime) -> bool:
        """
        Will insert a new row with the datetime provided as the punch in.

        Parameters
        ----------
        datetime_obj : datetime, required
            The datetime to record the punch in.

        Returns
        -------
        bool
            True on successful insert.
        """
        sql = 'UPDATE punches SET clock_in=? WHERE id=?'
        return self._update_punch(datetime_obj, sql)

    def start(self, datetime_obj: datetime) -> bool:
        """
        Will update the row for the time that lunch started.

        Parameters
        ----------
        datetime_obj : datetime, required
            The datetime to record the start of lunch.

        Returns
        -------
        bool
            True on successful update.
        """
        sql = 'UPDATE punches SET lunch_start=? WHERE id=?'
        return self._update_punch(datetime_obj, sql)

    def end(self, datetime_obj: datetime) -> bool:
        """
        Will update the row for the time that lunch ended.

        Parameters
        ----------
        datetime_obj : datetime, required
            The datetime to record the end of lunch.

        Returns
        -------
        bool
            True on successful update.
        """
        sql = 'UPDATE punches SET lunch_end=? WHERE id=?'
        return self._update_punch(datetime_obj, sql)

    def out(self, datetime_obj: datetime) -> bool:
        """
        Will update the row for the time that the day ended.

        Parameters
        ----------
        datetime_obj : datetime, required
            The datetime to record the day is done.

        Returns
        -------
        bool
            True on successful update.
        """
        sql = 'UPDATE punches SET clock_out=? WHERE id=?'
        return self._update_punch(datetime_obj, sql)

    def insert_new_day(self) -> bool:
        """
        Adds a new day to the datatable for tracking if there needs punches or
        for skipping the day entirely.

        Returns
        -------
        bool
            True on successful insert, false otherwise.
        """
        sql = 'INSERT INTO punches(punch_day) VALUES(?)'
        data = (date.today(),)

        try:
            self._connection.execute(sql, data)
            self._connection.commit()
        except sqlite3.OperationalError:
            return False

        return True

    def get_most_recent_day(self) -> tuple:
        """
        This will return the last row inserted into the table.

        Returns
        -------
        tuple
            Returns a tuple of the row of data.
        """
        sql = 'SELECT * FROM punches ORDER BY id DESC LIMIT 1'

        try:
            self._connection.execute(sql)
        except sqlite3.OperationalError:
            return ()
        
        return self._connection.fetchone()

    def is_work_day(self) -> bool:
        """Returns whether today is a work day or not."""
        return self.get_most_recent_day()[2]

    def update_is_work_day(self, is_work_day: bool) -> bool:
        """
        This will update the punch day to avoid checking if we need to clock in
        and out but only once based on weekends, holidays, or PTO days.

        Parameters
        ----------
        is_work_day : bool, required
            This is whether it is a valid day to punch in or not.

        Returns
        -------
        bool
            True on successful update, False otherwise.
        """
        sql = 'UPDATE punches SET is_work_day=? WHERE id=?'
        data = (is_work_day, self.get_most_recent_day()[0],)

        try:
            self._connection.execute(sql, data)
            self._connection.commit()
        except sqlite3.OperationalError:
            return False

        return True

    def _update_punch(self, datetime_obj: datetime, sql: str) -> bool:
        """
        Will run the given sql with the datetime, updating the most recently
        inserted row in the table for the given punch, passed in via the sql.

        Parameters
        ----------
        datetime_obj : datetime, required
            The date to insert into the column.

        sql : string, required
            The sql for the column to update.

        Returns
        -------
        bool
            True on successful update, false otherwise.
        """
        id_ = self.get_most_recent_day()[0]
        data = (datetime_obj, id_,)

        try:
            self._connection.execute(sql, data)
            self._connection.commit()
        except sqlite3.OperationalError:
            return False

        return True
