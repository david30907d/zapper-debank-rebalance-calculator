import pandas as pd

from rebalance_server.metrics.historical_price_reader import get_historical_price_reader
from rebalance_server.metrics.lp_token import calculate_historical_price_of_lp_token


def calculate_max_drawdown(categorized_positions_with_token_balance: dict):
    """Calculate the maximum drawdown of a portfolio.

    Args:
        categorized_positions_with_token_balance (dict): A dictionary of categorized_positions_with_token_balance in the portfolio. The keys are
            the ticker symbols and the values are the token balance.

    Returns:
        float: The maximum drawdown of the portfolio.
    """
    net_worth_series = pd.Series(dtype=float)
    historical_price_reader = get_historical_price_reader(source="coingecko")
    for lp_token in categorized_positions_with_token_balance.values():
        historical_price_per_lp_token: pd.Series = (
            calculate_historical_price_of_lp_token(lp_token, historical_price_reader)
        )
        if net_worth_series.empty:
            net_worth_series = historical_price_per_lp_token
        else:
            net_worth_series = net_worth_series.add(historical_price_per_lp_token)
    return (net_worth_series.max() - net_worth_series.min()) / net_worth_series.max()
