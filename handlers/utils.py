def place_value_into_categorized_portfolio_dict(
    categories: list,
    net_usd_valud: float,
    length_of_categories: int,
    symbol: str,
    apr: float,
    metadata: dict,
    tokens_metadata: list,
    result: dict,
):
    for category in categories:
        weighted_balanceUSD = net_usd_valud / length_of_categories
        result[category]["portfolio"][symbol]["worth"] += weighted_balanceUSD
        result[category]["portfolio"][symbol]["APR"] = apr
        result[category]["portfolio"][symbol]["metadata"] = metadata
        result[category]["portfolio"][symbol]["tokens_metadata"] = tokens_metadata
        result[category]["sum"] += weighted_balanceUSD
    return result
