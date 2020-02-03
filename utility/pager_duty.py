from smtplib import SMTP_SSL


class PagerDuty:
    """A class responsible for pager duty, sending alerts.

    Attributes
    ----------
    _from : string
        The e-mail address for login, and the from address.

    _to : string
        The text number using e-mail that will receive the alert.

    _server : SMTP_SSL
        The e-mail server that will be connected to, for sending messages.

    Methods
    -------
    _page(level, message)
        Logs into e-mail, and sends message.
    
    alert(message)
        Sends an alert level message when something goes wrong.

    warning(message)
        Sends an alert level message when something goes wrong.

    info(message)
        Sends an info message for record keeping
    """

    def __init__(self, config):
        """
        Creates a new instance of the PagerDuty object.

        Parameters
        ----------
        config : Config
            Configuration object that loaded the .env file.
        """
        pager_duty_info = config.get_pager_duty_info()

        self._from = pager_duty_info['from']
        self._to = pager_duty_info['to']

        self._server = SMTP_SSL('smtp.gmail.com', 465)
        self._server.login(self._from.split('@')[0], pager_duty_info['password'])

    def _page(self, level, message):
        """
        This method signs into the Google server, and send the text message
        to the provided phone number.

        Parameters
        ----------
        level : string, required
            The level of the message.

        message: string, required
            The message to be sent which is the core of the information.
        """
        body = 'Level - ' + level + '\nMessage - ' + message
        self._server.sendmail(self._from, self._to, body)

    def alert(self, message):
        """
        Sends an ALERT message out for when things go wrong.

        Parameters
        ----------
        message: string, required
            The message to be sent which is the core of the information.
        """
        self._page('ALERT', message)

    def warning(self, message):
        """
        Sends an WARNING message out for when things go wrong, but do
        warrant immediate action.

        Parameters
        ----------
        message: string, required
            The message to be sent which is the core of the information.
        """
        self._page('WARNING', message)

    def info(self, message):
        """
        Sends an INFO message out for when things go fine.

        Parameters
        ----------
        message: string, required
            The message to be sent which is the core of the information.
        """
        self._page('INFO', message)
