import pandas as pd


def calculate_daily_return_per_lp_token(
    lp_token: str, historical_price_reader: object
) -> pd.Series:
    # TODO(david): need to implement these 2
    # calculate_historical_apr_of_lp_token
    # calculate_historical_IL_of_lp_token
    return calculate_historical_price_of_lp_token(lp_token, historical_price_reader)


def calculate_historical_price_of_lp_token(
    lp_token: str, historical_price_reader: object
) -> pd.Series:
    """Calculate the historical price of a LP token.
    Args:
        lp_token (str): The LP token.
        historical_price_reader (object): The historical price reader.
    Returns:
        pd.Series: The historical price of the LP token.
    """
    series = pd.Series(dtype=float)
    for base_token in lp_token:
        tokenBalance = base_token["balance"]
        if _filter_for_token_balance(base_token):
            continue
        symbols_for_reader = (
            historical_price_reader.convert_symbol_from_dashboard_to_api_version(
                base_token["symbol"]
            )
        )
        for symbol in symbols_for_reader:
            price_pd = historical_price_reader.get_token_historical_price(symbol)
            if len(series) == 0:
                series = price_pd * tokenBalance
            else:
                series = series.add(price_pd * tokenBalance).dropna()
    # reverse the price series
    # Why: because the price series is in timestamp descending order, but every financial metrics need to be calculated in ascending order
    # In other words, [0] stands for the latest price, and [len(series)-1] stands for the earliest price
    return series


def _filter_for_token_balance(base_token: dict) -> bool:
    if base_token["balance"] < 10 and "eth" not in base_token["symbol"].lower():
        return True
    return False
