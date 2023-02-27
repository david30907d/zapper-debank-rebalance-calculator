import numpy as np
import pandas as pd

from metrics.utils import DAY_TIMEDELTA, get_token_historical_price


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
    daily_return_percentages = _get_daily_return_percentage_array(positions)
    # why multiply by sqrt(DAY_TIMEDELTA) ? Assumed that there's DAY_TIMEDELTA trading days. And since denomitor is daily's std. daily stuff is already under the effect of sqrt, so need to multply with sqrt(DAY_TIMEDELTA) to make it back to annualized
    return (
        np.sqrt(DAY_TIMEDELTA)
        * (daily_return_percentages["daily_return_percentages"].mean() - risk_free_rate)
        / daily_return_percentages["daily_return_percentages"].std()
    )


def _get_daily_return_percentage_array(positions: dict):
    df = pd.DataFrame()
    for symbol, tokenBalance in positions.items():
        price_pd = get_token_historical_price(symbol)
        daily_return_percentages_per_token = (
            _calculate_daily_return_percentages_per_token(price_pd, tokenBalance)
        )
        if "daily_return_percentages" not in df:
            df["daily_return_percentages"] = daily_return_percentages_per_token
        else:
            # `add` would auto truncate the NaN rows, making the length of the series equal
            df["daily_return_percentages"].add(daily_return_percentages_per_token)
    return df.dropna()


def _calculate_daily_return_percentages_per_token(price_pd, tokenBalance):
    return price_pd.pct_change() * price_pd * tokenBalance