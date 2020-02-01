import sqlite3


class Database:
    """A class that will handle Database interactions. 
    
    The connection to the database will be managed by this class object. No ORM
    will be used as there are very few interactions.

    Attributes
    ----------
    _cursor : Cursor
        The cursor for the database.

    _db : Connection
        A connection to the Database

    Methods
    -------
    get_cursor()
        Returns the cursor with the connection to the database.

    commit()
        Calls to commit the transaction.

    execute(sql, data)
        Executes the sequel.

    fetchall()
        After executing the sql, call fetch to get the models.

    fetchone()
        After executing the sql, call fetch to return only model.

    get_last_row_id()
        On an insert, this will return the new row id if applicable.
    """

    def __init__(self, config):
        """
        Creates a new instance of the Database object.

        Parameters
        ----------
        config : Config
            Configuration object that loaded the .env file.
        """
        self._db = sqlite3.connect(
            config.get_db_path(),
            check_same_thread=False
        )
        self._cursor = self._db.cursor()
    
    def commit(self):
        """Commits the database transactions."""
        self._db.commit()

    def execute(self, sql, data=()):
        """
        Executes the provided sql statement with the given data.

        Parameters
        --------
        sql : string, required
            The query to be executed.

        data : tuple, optional
             The data to be inserted into the sql statement.
        """
        self._cursor.execute(sql, data)

    def fetchall(self):
        """
        After executing the query, this will return the data.

        Return
        -------
        list
            The list of data returned from the query.
        """
        return self._cursor.fetchall()

    def fetchone(self):
        """
        After executing the query, this will return the data.

        Return
        -------
        tuple
            The list of data returned from the query.
        """
        return self._cursor.fetchone()
    
    def get_last_row_id(self):
        """
        Will return the last row id, generally used after an insert

        Return
        -------
        int
            The value of the last row inserted.
        """
        return self._cursor.lastrowid
