from datetime import datetime, timedelta
from pages import Dashboard, Login
from unittest.mock import Mock, patch
import pytest


# Unit under test
from utility import PunchCardManager


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
