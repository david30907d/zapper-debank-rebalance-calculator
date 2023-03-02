import datetime

# TODO: once data is enough,
DAY_TIMEDELTA = 365 * 4
# DAY_TIMEDELTA = 100


def get_required_unix_timestamp():
    # get the current date and time
    now = datetime.datetime.now()
    # calculate the date and time 90 days ago
    delta = datetime.timedelta(days=DAY_TIMEDELTA)
    days_ago = now - delta
    # convert the date and time to a Unix timestamp
    return int(days_ago.timestamp()), int(now.timestamp())


FOUR_YEARS_AGO_UNIX_TIMESTAMP, TODAY_UNIX_TIMESTAMP = get_required_unix_timestamp()
