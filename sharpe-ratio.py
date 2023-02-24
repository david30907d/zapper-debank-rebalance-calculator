import datetime, requests
import numpy as np
import pandas as pd

POSITIONS = {
    "governance-ohm": 17000, 
    "ethereum": 10000
}
# DAY_TIMEDELTA = 365 * 4
DAY_TIMEDELTA = 90
def get_required_unix_timestamp():
    # get the current date and time
    now = datetime.datetime.now()
    # calculate the date and time 90 days ago
    delta = datetime.timedelta(days=DAY_TIMEDELTA)
    days_ago = now - delta
    # convert the date and time to a Unix timestamp
    return int(days_ago.timestamp()),  int(now.timestamp())
FOUR_YEARS_AGO_UNIX_TIMESTAMP, TODAY_UNIX_TIMESTAMP = get_required_unix_timestamp()

def calculate_portfolio_sharpe_ratio(positions: dict, risk_free_rate: float = 0.0) -> float:
    """Calculate the Sharpe ratio of a portfolio.

    Args:
        positions (dict): A dictionary of positions in the portfolio. The keys are
            the ticker symbols and the values are the net worth.
        risk_free_rate (float, optional): The risk free rate of return. Defaults
            to 0.0.

    Returns:
        float: The Sharpe ratio of the portfolio.
    """
    daily_returns = _get_daily_returns(positions)
    return np.sqrt(DAY_TIMEDELTA) * daily_returns['daily_returns'].mean() / daily_returns['daily_returns'].std()

def _get_daily_returns(positions: dict):
    df = pd.DataFrame()
    for symbol, balanceUSD in positions.items():
        price_pd = _get_token_historical_price(symbol)
        daily_returns_per_token = _calculate_daily_returns_per_token(price_pd, balanceUSD)
        if 'daily_returns' not in df:
            df['daily_returns'] = daily_returns_per_token
        # `add` would auto truncate the NaN rows, making the length of the series equal
        df['daily_returns'].add(daily_returns_per_token)
    return df.dropna()

def _get_token_historical_price(symbol: str) -> pd.Series:
    res = requests.get(f'https://api.coingecko.com/api/v3/coins/{symbol}/market_chart/range?vs_currency=usd&from={FOUR_YEARS_AGO_UNIX_TIMESTAMP}&to={TODAY_UNIX_TIMESTAMP})')
    price = np.array(res.json()['prices'])[:,1]
    return pd.Series(price)

def _calculate_daily_returns_per_token(price_pd, balanceUSD):
    return price_pd.pct_change() * balanceUSD

if __name__ == "__main__":
    print(calculate_portfolio_sharpe_ratio(POSITIONS))