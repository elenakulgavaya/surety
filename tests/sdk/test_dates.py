from datetime import date, datetime, timedelta, timezone

from surety.sdk import dates


def test_get_current_time_utc():
    current_time = datetime.now(timezone.utc)
    got_time = dates.get_current_time_utc()
    assert got_time - current_time < timedelta(seconds=3)


def test_generate_date():
    got_date = dates.generate_date()
    assert isinstance(got_date, date)


def test_to_timestamp():
    current_time = datetime.now(timezone.utc)
    got_ts = dates.to_timestamp(current_time)
    assert isinstance(got_ts, int)


def test_to_format():
    date_time = datetime.fromisoformat('2023-02-16 21:32')
    got_str = dates.to_format(date_time)
    assert got_str == '2023-02-16T21:32:00Z'

def test_str_to_date():
    got_date = dates.str_to_date('2021-04-21', dates.Pattern.DATE)
    assert isinstance(got_date, datetime)


def test_to_timezone():
    current_time = datetime.now(timezone.utc)
    got_datetime = dates.to_timezone(current_time, 'US/Eastern')
    assert got_datetime.tzinfo.zone == 'US/Eastern'
