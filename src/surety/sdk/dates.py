import calendar
import random

from datetime import datetime, timezone

import pytz


DATE_TIME_PATTERN = '%Y-%m-%dT%H:%M:%SZ'


class Pattern:
    DATE = '%Y-%m-%d'
    TIME = '%H:%M:%S'
    DATETIME = '%Y-%m-%d %H:%M:%S'
    DATETIME_DELIM_T = '%Y-%m-%dT%H:%M:%S'
    DATETIME_DELIM_T_WITH_ZONE = '%Y-%m-%dT%H:%M:%SZ'
    DATETIME_DELIM_T_WITH_ZONE_PRECISED = '%Y-%m-%dT%H:%M:%S.%fZ'


def get_current_time_utc():
    return datetime.now(timezone.utc)


def generate_time():
    now = datetime.now(timezone.utc)

    return now.replace(
        day=random.randint(1, now.day),
        hour=random.randint(0, now.hour),
        minute=random.randint(0, now.minute),
        second=random.randint(0, now.second),
    )


def generate_date():
    time = generate_time()

    return datetime.date(time)


def to_format(date_time, pattern=Pattern.DATETIME_DELIM_T_WITH_ZONE):
    return date_time.strftime(pattern)


def to_timestamp(date_time):
    return int(calendar.timegm(date_time.utctimetuple()))


def str_to_date(date_string, pattern=Pattern.DATETIME_DELIM_T_WITH_ZONE):
    return datetime.strptime(date_string, pattern)


def to_timezone(date_time, tz):
    return date_time.astimezone(pytz.timezone(tz))
