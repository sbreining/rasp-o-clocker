class Punch:
    """A class that will handle Database interactions with the holidays table. 

    Attributes
    ----------
    _connection : Database
        A connection to the Database.

    Methods
    -------
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
