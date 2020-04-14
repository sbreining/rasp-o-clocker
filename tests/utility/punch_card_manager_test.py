from datetime import datetime, timedelta
from src.pages import Dashboard, Login
from selenium.common.exceptions import NoSuchElementException
from unittest.mock import Mock, patch
import pytest


# Unit under test
from src.utility import PunchCardManager


START_HOUR = 8


@pytest.fixture()
def args():
    config = Mock()
    config.get_start_hour = Mock(return_value=START_HOUR)

    return {
        'config': config,
        'driver': Mock(),
        'holiday': Mock(),
        'pager': Mock(),
        'punch': Mock()
    }


def test_start_inserts_new_day_if_db_is_empty(args):
    punch = Mock()
    punch.get_most_recent_day = Mock(return_value=None)
    # Inserting a new day will raise so that we do not enter infinite loop.
    punch.insert_new_day = Mock(side_effect=Exception())
    args['punch'] = punch

    pcm = PunchCardManager(args)

    try:
        pcm.start()
    except Exception:
        # Do nothing with exception
        pass

    punch.get_most_recent_day.assert_called_once()
    punch.insert_new_day.assert_called_once()


def test_start_inserts_new_day_if_most_recent_was_yesterday(args):
    yesterday = datetime.now().date() - timedelta(days=1)
    yesterday_str = yesterday.strftime('%Y-%m-%d')

    punch = Mock()
    punch.get_most_recent_day = Mock(return_value=(1, yesterday_str))
    # Inserting a new day will raise so that we do not enter infinite loop.
    punch.insert_new_day = Mock(side_effect=Exception())

    args['punch'] = punch

    pcm = PunchCardManager(args)

    try:
        pcm.start()
    except Exception:
        # Do nothing with exception
        pass

    assert punch.get_most_recent_day.call_count is 2
    punch.insert_new_day.assert_called_once()


@patch('time.sleep')
def test_start_sleeps_for_five_min_on_not_clock_day(time, args):
    # To break out of the infinite loop, we'll have sleep raise
    time.side_effect = [None, Exception()]

    punch = Mock()
    punch.get_most_recent_day = Mock(return_value=['a', 'b'])

    args['punch'] = punch

    pcm = PunchCardManager(args)
    pcm.get_datetime_from_date_string = Mock(return_value=datetime.now())
    pcm.is_clock_in_day = Mock(return_value=False)
    pcm.perform_action = Mock()
    pcm.should_punch = Mock()

    try:
        pcm.start()
    # Catching this exception is exiting the loop on the second sleep call.
    except Exception:
        # Do nothing with the exception
        pass

    time.assert_called_with(300)
    pcm.perform_action.assert_not_called()
    pcm.should_punch.assert_not_called()


@patch('time.sleep')
def test_start_performs_clock_in(time, args):
    # To break out of the infinite loop, we'll have sleep raise
    time.side_effect = Exception()

    today_str = datetime.now().date().strftime('%Y-%m-%d')

    punch = Mock()
    punch.get_most_recent_day = Mock(return_value=(1, today_str, None, None))

    args['punch'] = punch

    config = Mock()
    config.get_start_hour = Mock(return_value=datetime.now().hour)

    args['config'] = config

    pcm = PunchCardManager(args)
    pcm.get_datetime_from_date_string = Mock(return_value=datetime.now())
    pcm.is_clock_in_day = Mock(return_value=True)
    pcm.perform_action = Mock()
    pcm.should_punch = Mock()

    try:
        pcm.start()
    except Exception:
        # Do nothing with the exception
        pass

    pcm.perform_action.call_args[0] is 'Clock In'
    pcm.perform_action.assert_called_once()
    pcm.should_punch.assert_not_called()
    time.assert_called_once_with(60)


@patch('time.sleep')
def test_start_performs_lunch_start(time, args):
    # To break out of the infinite loop, we'll have sleep raise
    time.side_effect = Exception()

    today_str = datetime.now().date().strftime('%Y-%m-%d')

    punch = Mock()
    punch.get_most_recent_day = Mock(return_value=(1, today_str, None, None))

    args['punch'] = punch

    pcm = PunchCardManager(args)
    pcm.get_datetime_from_date_string = Mock(return_value=datetime.now())
    pcm.is_clock_in_day = Mock(return_value=True)
    pcm.perform_action = Mock()
    pcm.should_punch = Mock(return_value=True)

    try:
        pcm.start()
    except Exception:
        # Do nothing with the exception
        pass

    pcm.perform_action.call_args[0] is 'Start Lunch'
    pcm.perform_action.assert_called_once()
    pcm.should_punch.assert_called_once()
    time.assert_called_once_with(60)


@patch('time.sleep')
def test_start_performs_end_lunch(time, args):
    # To break out of the infinite loop, we'll have sleep raise
    time.side_effect = Exception()

    today_str = datetime.now().date().strftime('%Y-%m-%d')

    punch = Mock()
    punch.get_most_recent_day = Mock(return_value=(1, today_str, None, None))

    args['punch'] = punch

    pcm = PunchCardManager(args)
    pcm.get_datetime_from_date_string = Mock(return_value=datetime.now())
    pcm.is_clock_in_day = Mock(return_value=True)
    pcm.perform_action = Mock()
    pcm.should_punch = Mock(side_effect=[False, True])

    try:
        pcm.start()
    except Exception:
        # Do nothing with the exception
        pass

    pcm.perform_action.call_args[0] is 'End Lunch'
    pcm.perform_action.assert_called_once()
    assert pcm.should_punch.call_count is 2
    time.assert_called_once_with(60)


@patch('time.sleep')
def test_start_performs_clock_out(time, args):
    # To break out of the infinite loop, we'll have sleep raise
    time.side_effect = Exception()

    today_str = datetime.now().date().strftime('%Y-%m-%d')

    punch = Mock()
    punch.get_most_recent_day = Mock(return_value=(1, today_str, None, None))

    args['punch'] = punch

    pcm = PunchCardManager(args)
    pcm.get_datetime_from_date_string = Mock(return_value=datetime.now())
    pcm.is_clock_in_day = Mock(return_value=True)
    pcm.perform_action = Mock()
    pcm.should_punch = Mock(side_effect=[False, False, True])

    try:
        pcm.start()
    except Exception:
        # Do nothing with the exception
        pass

    pcm.perform_action.call_args[0] is 'Clock Out'
    pcm.perform_action.assert_called_once()
    assert pcm.should_punch.call_count is 3
    time.assert_called_once_with(60)


def test_login_to_paylocity_returns_dashboard(args):
    pcm = PunchCardManager(args)

    question_page = Mock()
    question_page.is_on_question_page = Mock(return_value=False)

    with patch.object(Login, 'login', return_value=question_page):
        dash = pcm.login_to_paylocity()

    assert isinstance(dash, Dashboard)


def test_login_to_paylocity_calls_answer_question(args):
    pcm = PunchCardManager(args)

    expected = Mock()

    question_page = Mock()
    question_page.is_on_question_page = Mock(return_value=True)
    question_page.answer_question = Mock(return_value=expected)

    with patch.object(Login, 'login', return_value=question_page):
        actual = pcm.login_to_paylocity()

    question_page.answer_question.assert_called_once()
    assert actual is expected


@pytest.mark.parametrize(
    'work_day_return,resource_return',
    [(True,None), (False,None), (None,True), (None,False)]
)
def test_is_clock_in_day_returns_bool(args, work_day_return, resource_return):
    punch = Mock()
    punch.is_work_day = Mock(return_value=work_day_return)
    punch.update_is_work_day = Mock()

    args['punch'] = punch

    now = datetime.now()

    pcm = PunchCardManager(args)
    pcm.check_resources = Mock(return_value=resource_return)

    actual = pcm.is_clock_in_day(now)

    if work_day_return is None:
        pcm.check_resources.assert_called_once_with(now)
        punch.update_is_work_day.assert_called_once_with(resource_return)
        assert actual is resource_return
    else:
        pcm.check_resources.assert_not_called()
        punch.update_is_work_day.assert_not_called()
        assert actual is work_day_return


@pytest.mark.parametrize(
    'date_str',
    [
        '2020-03-19',  # Friday
        '2020-03-21',  # Saturday
        '2020-03-22'   # Sunday
    ]
)
def test_check_resources_returns_false_for_weekend_or_holiday(args, date_str):
    holiday = Mock()
    holiday.is_holiday = Mock(return_value=True)

    args['holiday'] = holiday

    date = datetime.strptime(date_str, '%Y-%m-%d')

    pcm = PunchCardManager(args)
    pcm.login_to_paylocity = Mock()

    actual = pcm.check_resources(date)

    pcm.login_to_paylocity.assert_not_called()
    assert actual is False


@pytest.mark.parametrize('is_pto_day_return', [(True,), (False,)])
def test_check_resources_returns_based_on_pto(args, is_pto_day_return):
    pto_mock = Mock()
    pto_mock.is_pto_day = Mock(return_value=is_pto_day_return)

    dash_mock = Mock()
    dash_mock.go_to_pto = Mock(return_value=pto_mock)

    holiday = Mock()
    holiday.is_holiday = Mock(return_value=False)

    args['holiday'] = holiday

    pcm = PunchCardManager(args)
    pcm.login_to_paylocity = Mock(return_value=dash_mock)

    now = Mock()
    now.weekday = Mock(return_value=3)  # Number is arbitrary, but less than 5

    actual = pcm.check_resources(now)

    assert actual is not is_pto_day_return


@pytest.fixture()
def dashboard():
    dashboard = Mock()
    dashboard.clock_in = Mock()
    dashboard.start_lunch = Mock()
    dashboard.end_lunch = Mock()
    dashboard.clock_out = Mock()

    return dashboard


@pytest.mark.parametrize('dash_fn', [
    'Clock In',
    'Start Lunch',
    'End Lunch',
    'Clock Out'
])
def test_perform_action_calls_dashboard_function(args, dashboard, dash_fn):
    pager = Mock()
    pager.info = Mock()

    args['pager'] = pager

    pcm = PunchCardManager(args)
    pcm.login_to_paylocity = Mock(return_value=dashboard)

    db_fn = lambda time: True

    now = datetime.now()

    pcm.perform_action(dash_fn, now, db_fn)

    info_msg = '%s at %s' % (dash_fn, now.strftime('%c'))
    pager.info.assert_called_once_with(info_msg)


def test_perform_action_calls_raises_and_alerts(args, dashboard):
    dashboard.clock_in.side_effect = NoSuchElementException()

    pager = Mock()
    pager.alert = Mock()

    args['pager'] = pager

    pcm = PunchCardManager(args)
    pcm.login_to_paylocity = Mock(return_value=dashboard)

    db_fn = lambda time: True

    pcm.perform_action('Clock In', datetime.now(), db_fn)

    alert_message = 'Did not Clock In successfully.'
    pager.alert.assert_called_once_with(alert_message)


def test_perform_action_calls_fails_db_and_warns(args, dashboard):
    pager = Mock()
    pager.warning = Mock()

    args['pager'] = pager

    pcm = PunchCardManager(args)
    pcm.login_to_paylocity = Mock(return_value=dashboard)

    db_fn = lambda time: False

    pcm.perform_action('Clock In', datetime.now(), db_fn)

    alert_message = 'Did not log Clock In to database'
    pager.warning.assert_called_once_with(alert_message)


def test_should_punch_returns_false_for_existing_punch(args):
    pcm = PunchCardManager(args)
    actual = pcm.should_punch(('Not none',), 0, 0, datetime.now(), timedelta(days=1))

    assert actual is False


def test_should_punch_returns_false_is_previous_punch_missing(args):
    punch_card = (None, None)
    pcm = PunchCardManager(args)
    actual = pcm.should_punch(punch_card, 0, 1, datetime.now(), timedelta(days=1))

    assert actual is False


@pytest.mark.parametrize('expected', [True, False])
def test_should_punch_returns_boolean_satisfying_delta_logic(args, expected):
    now = datetime.now()
    earlier = now - timedelta(hours=2) if expected else now - timedelta(minutes=10)
    earlier_str = earlier.strftime('%Y-%m-%d %H:%M:%S.%f')

    punch_card = (earlier_str, None)
    pcm = PunchCardManager(args)
    actual = pcm.should_punch(punch_card, 0, 1, now, timedelta(hours=1))

    assert actual is expected