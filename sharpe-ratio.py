import datetime
import json

import numpy as np
import pandas as pd
import requests

POSITIONS = {
    "governance-ohm": 10,
    # "ethereum": 10
}
# TODO: once data is enough,
# DAY_TIMEDELTA = 365 * 4
DAY_TIMEDELTA = 100


def get_required_unix_timestamp():
    # get the current date and time
    now = datetime.datetime.now()
    # calculate the date and time 90 days ago
    delta = datetime.timedelta(days=DAY_TIMEDELTA)
    days_ago = now - delta
    # convert the date and time to a Unix timestamp
    return int(days_ago.timestamp()), int(now.timestamp())


FOUR_YEARS_AGO_UNIX_TIMESTAMP, TODAY_UNIX_TIMESTAMP = get_required_unix_timestamp()


def calculate_portfolio_sharpe_ratio(
    positions: dict, risk_free_rate: float = 0.0
) -> float:
    """Calculate the Sharpe ratio of a portfolio.

    Args:
        positions (dict): A dictionary of positions in the portfolio. The keys are
            the ticker symbols and the values are the token balance.
        risk_free_rate (float, optional): The risk free rate of return. Defaults
            to 0.0.

    Returns:
        float: The Sharpe ratio of the portfolio.
    """
    daily_returns = _get_daily_returns(positions)
    # why multiply by sqrt(DAY_TIMEDELTA) ? Assumed that there's DAY_TIMEDELTA trading days. And since denomitor is daily's std. daily stuff is already under the effect of sqrt, so need to multply with sqrt(DAY_TIMEDELTA) to make it back to annualized
    return (
        np.sqrt(DAY_TIMEDELTA)
        * daily_returns["daily_returns"].mean()
        / daily_returns["daily_returns"].std()
    )


def calculate_max_drawdown(positions: dict):
    """Calculate the maximum drawdown of a portfolio.

    Args:
        positions (dict): A dictionary of positions in the portfolio. The keys are
            the ticker symbols and the values are the token balance.

    Returns:
        float: The maximum drawdown of the portfolio.
    """
    net_worth = pd.DataFrame()
    for symbol, tokenBalance in positions.items():
        price_pd = _get_token_historical_price(symbol)
        if "net_worth" not in net_worth:
            net_worth["net_worth"] = price_pd * tokenBalance
        else:
            net_worth["net_worth"].add(price_pd * tokenBalance)
    return (net_worth["net_worth"].max() - net_worth["net_worth"].min()) / net_worth[
        "net_worth"
    ].max()


def _get_daily_returns(positions: dict):
    df = pd.DataFrame()
    for symbol, tokenBalance in positions.items():
        price_pd = _get_token_historical_price(symbol)
        daily_returns_per_token = _calculate_daily_returns_per_token(
            price_pd, tokenBalance
        )
        if "daily_returns" not in df:
            df["daily_returns"] = daily_returns_per_token
        else:
            # `add` would auto truncate the NaN rows, making the length of the series equal
            df["daily_returns"].add(daily_returns_per_token)
    return df.dropna()


def _get_token_historical_price(symbol: str) -> pd.Series:
    res = requests.get(
        f"https://api.coingecko.com/api/v3/coins/{symbol}/market_chart/range?vs_currency=usd&from={FOUR_YEARS_AGO_UNIX_TIMESTAMP}&to={TODAY_UNIX_TIMESTAMP})"
    )
    print(res.json())
    if res.status_code == 200:
        json.dump(res.json(), open(f"{symbol}.json", "w"))
    price = np.array(res.json()["prices"])[:, 1]
    res = json.load(open(f"{symbol}.json", "r"))
    price = np.array(res["prices"])[:, 1]
    return pd.Series(price)


def _calculate_daily_returns_per_token(price_pd, tokenBalance):
    return price_pd.pct_change() * price_pd * tokenBalance


if __name__ == "__main__":
    print(f"sharpe index: {calculate_portfolio_sharpe_ratio(POSITIONS)}")
    print(f"max drawdown: {calculate_max_drawdown(POSITIONS)}")

# TODO: need to calculate LP's price + GLP's price
