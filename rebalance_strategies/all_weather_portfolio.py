from utils.position import skip_rebalance_if_position_too_small


def all_weather_portfolio(category, portfolio, net_worth):
    target_asset_allocation = {
        "long_term_bond": 0.4,
        "intermediate_term_bond": 0.15,
        "commodities": 0.075,
        "gold": 0.075,
        "large_cap_us_stocks": 0.18,
        "small_cap_us_stocks": 0.03,
        "non_us_developed_market_stocks": 0.06,
        "non_us_emerging_market_stocks": 0.03,
    }
    target_sum = net_worth * target_asset_allocation[category]
    print(
        f"Current {category}: {portfolio['sum']:.2f}",
        f"Target Sum: {target_sum:.2f}",
        f"Investment Shift: {(portfolio['sum']-target_sum)/net_worth:.2f}, should be lower than 0.05",
    )
    diffrence = target_sum - portfolio["sum"]
    for symbol, position_obj in sorted(
        portfolio["portfolio"].items(), key=lambda x: -x[1]["worth"]
    ):
        balanceUSD = position_obj["worth"]
        if skip_rebalance_if_position_too_small(balanceUSD):
            continue
        print(
            f"Suggestion: modify this amount of USD: {diffrence * balanceUSD / portfolio['sum']:.2f} for position {symbol}, current worth: {balanceUSD:.2f}, percentage: {balanceUSD/net_worth:.2f}"
        )
