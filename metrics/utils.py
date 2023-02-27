import datetime
import json

import numpy as np
import pandas as pd
import requests

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


def get_token_historical_price(symbol: str) -> pd.Series:
    res = requests.get(
        f"https://api.coingecko.com/api/v3/coins/{symbol}/market_chart/range?vs_currency=usd&from={FOUR_YEARS_AGO_UNIX_TIMESTAMP}&to={TODAY_UNIX_TIMESTAMP})"
    )
    if res.status_code == 200:
        json.dump(res.json(), open(f"{symbol}.json", "w"))
    price = np.array(res.json()["prices"])[:, 1]
    res = json.load(open(f"{symbol}.json", "r"))
    price = np.array(res["prices"])[:, 1]
    return pd.Series(price)
