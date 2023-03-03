import numpy as np
import pandas as pd

from adapters.networth_to_balance_adapter import get_networh_to_balance_adapter
from metrics.historical_price_reader import get_historical_price_reader
from metrics.lp_token import calculate_historical_price_of_lp_token
from metrics.utils import DAY_TIMEDELTA


def calculate_portfolio_sharpe_ratio(
    categorized_positions: dict, risk_free_rate: float = 0.0
) -> float:
    """Calculate the Sharpe ratio of a portfolio.

    Args:
        categorized_positions (dict): A dictionary of categorized_positions in the portfolio. The keys are
            the ticker symbols and the values are the token balance.
        risk_free_rate (float, optional): The risk free rate of return. Defaults
            to 0.0.

    Returns:
        float: The Sharpe ratio of the portfolio.
    """
    adapter = get_networh_to_balance_adapter(adapter="coingecko")
    categorized_positions_with_token_balance = adapter(categorized_positions)
    daily_return_percentages = _get_daily_return_percentage_array(
        categorized_positions_with_token_balance
    )
    # why multiply by sqrt(DAY_TIMEDELTA) ? Assumed that there's DAY_TIMEDELTA trading days. And since denomitor is daily's std. daily stuff is already under the effect of sqrt, so need to multply with sqrt(DAY_TIMEDELTA) to make it back to annualized
    return (
        np.sqrt(DAY_TIMEDELTA)
        * (daily_return_percentages.mean() - risk_free_rate)
        / daily_return_percentages.std()
    )


def _get_daily_return_percentage_array(
    categorized_positions_with_token_balance: dict,
) -> pd.Series:
    series = pd.Series(dtype=float)
    historical_price_reader = get_historical_price_reader(source="coingecko")
    for lp_token in categorized_positions_with_token_balance.values():
        # TODO: too hard to implement, wait for next sprint
        # V0 would only focus on base-token's historical price
        price_pd_of_lp_token: pd.Series = calculate_historical_price_of_lp_token(
            lp_token, historical_price_reader
        )
        daily_return_percentages_per_lp_token = (
            _calculate_daily_return_percentages_per_lp_token(price_pd_of_lp_token)
        )
        if len(series) == 0:
            series = daily_return_percentages_per_lp_token
        else:
            series = series.add(daily_return_percentages_per_lp_token)
    return series


def _calculate_daily_return_percentages_per_lp_token(price_pd: pd.Series):
    return price_pd.pct_change()
