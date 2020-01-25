import sqlite3
from calendar import month_name


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
        self._cursor = self._db.cursor()
    
    def commit(self):
        self._db.commit()

    def execute(self, sql, data):
        self._cursor.execute(sql, data)

    def fetchall(self):
        return self._cursor.fetchall()
    
    def get_last_row_id(self):
        return self._cursor.lastrowid
