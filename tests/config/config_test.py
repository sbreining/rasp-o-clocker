# Unit under test
from config import Config


def test_get_login_returns_credentials(monkeypatch):
    monkeypatch.setenv('COMPANY_CODE', 'someId')
    monkeypatch.setenv('USERNAME', 'someUsername')
    monkeypatch.setenv('PASSWORD', 'somePassword')

    expected = {
        'companyId': 'someId',
        'username': 'someUsername',
        'password': 'somePassword'
    }

    login = Config.get_login()

    assert login == expected


def test_get_login_url_returns_url_string(monkeypatch):
    monkeypatch.setenv('PAYLOCITY_LOGIN_URL', 'someUrl')

    assert Config.get_login_url() == 'someUrl'


def test_get_dashboard_url_returns_url_string(monkeypatch):
    monkeypatch.setenv('PAYLOCITY_BASE_URL', 'someDashboardUrl')

    assert Config.get_dashboard_url() == 'someDashboardUrl'


def test_get_implicit_wait_returns_number_of_seconds(monkeypatch):
    monkeypatch.setenv('IMPLICIT_WAIT', '10')

    assert Config.get_implicit_wait() == 10


def test_get_db_path_returns_file_path_to_dotdb_file():
    assert 'database.db' in Config.get_db_path()


def test_get_questions_returns_dictionary_of_questions_answers(monkeypatch):
    monkeypatch.setenv('SECRET_Q_1', 'q1')
    monkeypatch.setenv('SECRET_Q_2', 'q2')
    monkeypatch.setenv('SECRET_Q_3', 'q3')
    monkeypatch.setenv('SECRET_A_1', 'a1')
    monkeypatch.setenv('SECRET_A_2', 'a2')
    monkeypatch.setenv('SECRET_A_3', 'a3')

    expected = {
        'q1': 'a1',
        'q2': 'a2',
        'q3': 'a3'
    }

    questions = Config.get_questions()

    assert questions == expected


def test_get_pager_duty_info_returns_dictionary(monkeypatch):
    monkeypatch.setenv('EMAIL_ADDRESS', 'email')
    monkeypatch.setenv('EMAIL_PASSWORD', 'password')
    monkeypatch.setenv('SMS_GATEWAY', 'phone')

    expected = {
        'from': 'email',
        'password': 'password',
        'to': 'phone'
    }

    pager_duty = Config.get_pager_duty_info()

    assert expected == pager_duty


def test_get_start_hour_returns_number(monkeypatch):
    monkeypatch.setenv('STARTING_HOUR', '8')

    assert Config.get_start_hour() == 8
