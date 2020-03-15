from datetime import datetime
from unittest.mock import Mock, patch
import pytest


# Unit under test
from utility import PunchCardManager


@pytest.fixture()
def args():
    return {
        'config': Mock(),
        'driver': Mock(),
        'holiday': Mock(),
        'pager': Mock(),
        'punch': Mock()
    }


@patch('time.sleep')
def test_start_sleeps_for_five_min_on_not_clock_day(time, args):
    # To break out of the infinite loop, we'll have sleep raise
    time.side_effect = Exception()

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
    except Exception:
        time.assert_called_once_with(300)

    pcm.perform_action.assert_not_called()
    pcm.should_punch.assert_not_called()
    pass


def test_start_performs_clock_in():
    pass


def test_start_performs_lunch_start():
    pass


def test_start_performs_end_lunch():
    pass


def test_start_performs_clock_out():
    pass