from unittest.mock import Mock
import pytest


# Unit under test
from utility import PagerDuty


username = 'some'
from_email = '%s@email.com' % username
password = 'secure password'
to_email = '8675309@cellprovider.net'
pager_duty_info = {
    'from': from_email,
    'password': password,
    'to': to_email
}
config = Mock()
config.get_pager_duty_info = Mock(return_value=pager_duty_info)


smtp = Mock()
smtp.connect = Mock()
smtp.login = Mock()
smtp.sendmail = Mock()
smtp.quit = Mock()


@pytest.mark.parametrize('log_level', ['alert', 'warning', 'info'])
def test_log_levels(log_level):
    pager_message = 'some message'

    pd = PagerDuty(config, smtp)

    switch = {
        'alert': pd.alert,
        'warning': pd.warning,
        'info': pd.info
    }

    switch[log_level](pager_message)

    smtp.connect.assert_called_once_with('smtp.gmail.com', 465)
    smtp.login.assert_called_once_with(username, password)

    expected = 'Level - %s\nMessage - %s' % (log_level.upper(), pager_message)
    smtp.sendmail.assert_called_once_with(from_email, to_email, expected)

    smtp.quit.assert_called_once()

    # Parameterized test needs the calls to be reset.
    smtp.reset_mock()
