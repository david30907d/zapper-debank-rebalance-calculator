import pandas as pd

from metrics.utils import get_token_historical_price


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
        price_pd = get_token_historical_price(symbol)
        if "net_worth" not in net_worth:
            net_worth["net_worth"] = price_pd * tokenBalance
        else:
            net_worth["net_worth"].add(price_pd * tokenBalance)
    return (net_worth["net_worth"].max() - net_worth["net_worth"].min()) / net_worth[
        "net_worth"
    ].max()
