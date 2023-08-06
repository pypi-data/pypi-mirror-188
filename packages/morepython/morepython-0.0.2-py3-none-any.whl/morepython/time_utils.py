import datetime
import re


def timestamp_to_microseconds(timestamp):
    """Convert RFC3339 timestamp to microseconds. This is needed since
        ``datetime.datetime.strptime()`` does not support nanosecond precision.
    :param timestamp: RFC3339 timestamp
    :type timestamp: str
    :return: The number of microseconds of the timestamp
    :rtype: int
    """

    info = list(filter(None, re.split(r'[\.|Z]{1}', timestamp))) + [0]
    return round((datetime.datetime.strptime(f'{info[0]}Z', '%Y-%m-%dT%H:%M:%SZ').timestamp() + float(f'0.{info[1]}')) * 1e6)


def time_to_seconds(time):
    """Convert timestamp string of the form 'hh:mm:ss' to seconds.
    :param time: Timestamp of the form 'hh:mm:ss'
    :type time: str
    :return: The corresponding number of seconds
    :rtype: int
    """
    if not time:
        return 0
    return int(sum(abs(int(x)) * 60 ** i for i, x in enumerate(reversed(time.replace(',', '').split(':')))) * (-1 if time[0] == '-' else 1))


def seconds_to_time(seconds, format='{}:{:02}:{:02}', remove_leading_zeroes=True):
    """Convert seconds to timestamp.
    :param seconds: Number of seconds
    :type seconds: int
    :param format: The format string with elements representing hours, minutes and seconds. Defaults to '{}:{:02}:{:02}'
    :type format: str, optional
    :param remove_leading_zeroes: Whether to remove leading zeroes when seconds > 60, defaults to True
    :type remove_leading_zeroes: bool, optional
    :return: The corresponding timestamp string
    :rtype: str
    """
    h, remainder = divmod(abs(int(seconds)), 3600)
    m, s = divmod(remainder, 60)
    time_string = format.format(h, m, s)
    return ('-' if seconds < 0 else '') + (re.sub(r'^0:0?', '', time_string) if remove_leading_zeroes else time_string)


def microseconds_to_timestamp(microseconds, format='%Y-%m-%d %H:%M:%S'):
    """Convert unix time to human-readable timestamp.
    :param microseconds: UNIX microseconds
    :type microseconds: float
    :param format: The format string, defaults to '%Y-%m-%d %H:%M:%S'. For
        information on supported codes, see https://strftime.org/ and
        https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
    :type format: str, optional
    :return: Human readable timestamp corresponding to the format
    :rtype: str
    """
    return datetime.datetime.fromtimestamp(microseconds // 1000000).strftime(format)
