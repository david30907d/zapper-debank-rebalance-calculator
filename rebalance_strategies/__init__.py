from rebalance_strategies.all_weather_portfolio import all_weather_portfolio
from rebalance_strategies.permanent_portfolio import permenant_portfolio


def output_rebalancing_suggestions(categorized_positions, strategy_name: str):
    strategy_fn = _get_rebalancing_strategy(strategy_name)
    net_worth = sum(portfolio["sum"] for portfolio in categorized_positions.values())
    for category, portfolio in categorized_positions.items():
        strategy_fn(category, portfolio, net_worth)
        print("====================")
    print(f"Current Net Worth: ${net_worth:.2f}")
    return net_worth


def _get_rebalancing_strategy(strategy_name: str) -> callable:
    if strategy_name == "permanent_portfolio":
        return permenant_portfolio
    elif strategy_name == "all_weather_portfolio":
        return all_weather_portfolio
    raise NotImplementedError(f"Strategy {strategy_name} is not implemented yet")
