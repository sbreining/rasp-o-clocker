from src.config import Config
from smtplib import SMTP_SSL


GMAIL_DOMAIN = 'smtp.gmail.com'
GMAIL_PORT = 465


class PagerDuty:
    """A class responsible for pager duty, sending alerts.

    Attributes
    ----------
    _from : string
        The e-mail address for login, and the from address.

    _password : string
        Password to login to the e-mail account.

    _to : string
        The text number using e-mail that will receive the alert.

    _email_server : SMTP_SSL
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

    def __init__(self, config: Config, smtp_ssl: SMTP_SSL):
        """
        Creates a new instance of the PagerDuty object.

        Parameters
        ----------
        config : Config
            Configuration object that loaded the .env file.
        """
        pager_duty_info = config.get_pager_duty_info()

        self._from = pager_duty_info['from']
        self._password = pager_duty_info['password']
        self._to = pager_duty_info['to']

        self._email_server = smtp_ssl

        self._has_email_credentials = True

        if not self._from or not self._password or not self._to:
            self._has_email_credentials = False

    def _page(self, level: str, message: str) -> None:
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
        body = 'Level - %s\nMessage - %s' % (level, message)
        if not self._has_email_credentials:
            print(body)
            return

        self._email_server.connect(GMAIL_DOMAIN, GMAIL_PORT)
        self._email_server.login(self._from.split('@')[0], self._password)
        self._email_server.sendmail(self._from, self._to, body)
        self._email_server.quit()

    def alert(self, message: str) -> None:
        """
        Sends an ALERT message out for when things go wrong.

        Parameters
        ----------
        message: string, required
            The message to be sent which is the core of the information.
        """
        self._page('ALERT', message)

    def warning(self, message: str) -> None:
        """
        Sends an WARNING message out for when things go wrong, but do
        warrant immediate action.

        Parameters
        ----------
        message: string, required
            The message to be sent which is the core of the information.
        """
        self._page('WARNING', message)

    def info(self, message: str) -> None:
        """
        Sends an INFO message out for when things go fine.

        Parameters
        ----------
        message: string, required
            The message to be sent which is the core of the information.
        """
        self._page('INFO', message)
