import datetime as dt
from typing import Optional, Iterator

import pendulum


def iter_range_datetime(
    start_time: pendulum.DateTime, end_time: pendulum.DateTime, timedelta: dt.timedelta
) -> Iterator[pendulum.DateTime]:
    if start_time > end_time:
        raise ValueError("start_time > end_time")

    while start_time <= end_time:
        yield start_time
        start_time += timedelta


def iter_range_datetime2(
    start_time: pendulum.DateTime, seconds: int, size: int
) -> Iterator[pendulum.DateTime]:
    for _ in range(size):
        yield start_time
        start_time += dt.timedelta(seconds=seconds)


def iter_period_from_range(
    datetimes: list[pendulum.DateTime],
    interval_timedelta: dt.timedelta,
    length: Optional[int] = None,
) -> Iterator[tuple[pendulum.DateTime, pendulum.DateTime]]:
    datetimes = sorted(set(datetimes))
    while datetimes:
        date1 = datetimes.pop(0)
        date2 = date1
        i = 1
        while datetimes:
            i += 1
            date = date2 + interval_timedelta
            if date in datetimes and (length is None or i <= length):
                date2 = datetimes.pop(datetimes.index(date))
            else:
                break

        yield date1, date2


def scroll_to_last_interval_time(
    start_time: pendulum.DateTime,
    interval_timedelta: dt.timedelta,
) -> pendulum.DateTime:
    return list(
        iter_range_datetime(start_time, pendulum.now(), timedelta=interval_timedelta)
    )[-1]


def strftime_utc(value: pendulum.DateTime) -> str:
    value = value.astimezone(pendulum.UTC)
    value = value.replace(tzinfo=None, microsecond=0)
    return value.isoformat()
