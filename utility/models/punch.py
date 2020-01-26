import sqlite3


class Punch:
    """A class that will handle Database interactions with the holidays table. 

    Attributes
    ----------
    _connection : Database
        A connection to the Database.

    _id : int
        The ID for the row that should be updated for a given day.

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
    """

    def __init__(self, connection):
        """
        Creates a new instance of the Punch model object.

        Parameters
        ----------
        connection : Database, required
            Holds on to database connection.
        """
        self._connection = connection
        self._id = 0

    def get_punch_by_id(self, id_):
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

        results = self._connection.fetchall()

        if len(results) == 0:
            return ()

        return results[0]

    def in_(self, datetime):
        """
        Will insert a new row with the datetime provided as the punch in.

        Parameters
        ----------
        datetime : datetime, required
            The datetime to record the punch in.

        Returns
        -------
        bool
            True on successful insert.
        """
        sql = 'INSERT INTO punches(clock_in) VALUES(?)'
        data = (datetime,)

        try:
            self._connection.execute(sql, data)
            self._connection.commit()
        except sqlite3.OperationalError:
            return False

        self._id = self._connection.get_last_row_id()

        return True

    def start(self, datetime):
        pass

    def end(self, datetime):
        pass

    def out(self, datetime):
        pass
