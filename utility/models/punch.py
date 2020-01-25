class Punch:
    """A class that will handle Database interactions with the holidays table. 

    Attributes
    ----------
    _cursor : Cursor
        A connection to the Database

    Methods
    -------
    """
    
    def __init__(self, connection):
        """
        Creates a new instance of the Punch model object.

        Parameters
        ----------
        config : Config, required
            Holds on to database connection credentials.
        """
        self._connection = connection

    