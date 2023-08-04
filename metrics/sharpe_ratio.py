import numpy as np
import pandas as pd

from rebalance_server.apr_utils.apr_calculator import get_lowest_or_default_apr
from rebalance_server.metrics.historical_price_reader import get_historical_price_reader
from rebalance_server.metrics.lp_token import calculate_daily_return_per_lp_token
from rebalance_server.metrics.utils import DAY_TIMEDELTA


def calculate_portfolio_sharpe_ratio(
    categorized_positions_with_token_balance: dict, risk_free_rate: float = 0.041
) -> float:
    """Calculate the Sharpe ratio of a portfolio.

    Args:
        categorized_positions (dict): A dictionary of categorized_positions in the portfolio. The keys are
            the ticker symbols and the values are the token balance.
        risk_free_rate (float, optional): The risk free rate of return. Defaults
            to 0.041, which is the APR of Lido

    Returns:
        float: The Sharpe ratio of the portfolio.
    """
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
    import json

    json.dump(
        categorized_positions_with_token_balance,
        open("categorized_positions_with_token_balance.json", "w"),
    )
    historical_price_reader = get_historical_price_reader(source="coingecko")
    for (
        addr_project_symbol,
        lp_token,
    ) in categorized_positions_with_token_balance.items():
        daily_return_per_lp_token: pd.Series = calculate_daily_return_per_lp_token(
            lp_token, historical_price_reader
        )
        daily_return_percentages_per_lp_token = (
            _calculate_daily_return_percentages_per_lp_token(daily_return_per_lp_token)
        )
        daily_return_percentages_with_farm_reward_per_lp_token = _add_farm_reward(
            addr_project_symbol, daily_return_percentages_per_lp_token
        )
        if series.empty:
            series = daily_return_percentages_with_farm_reward_per_lp_token
        else:
            series = series.add(
                daily_return_percentages_with_farm_reward_per_lp_token
            ).dropna()
    return series


def _calculate_daily_return_percentages_per_lp_token(price_pd: pd.Series):
    return price_pd.pct_change()


def _add_farm_reward(
    addr_project_symbol: str, daily_return_percentages_per_lp_token: pd.Series
):
    splitted_data = addr_project_symbol.split(":")
    addr_with_metadata = ":".join(splitted_data[:-2])
    project, symbol = splitted_data[-2], splitted_data[-1]
    address_project = f"{addr_with_metadata}:{project}"
    project_symbol = f"{project}:{symbol}"
    apr = get_lowest_or_default_apr(project_symbol, address_project)
    return daily_return_percentages_per_lp_token * (1 + apr / 365)
