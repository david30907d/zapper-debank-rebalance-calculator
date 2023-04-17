from rebalance_strategies.all_weather_portfolio import AllWeatherPortfolio
from rebalance_strategies.permanent_portfolio import PermanentPortfolio


def get_rebalancing_suggestions(
    categorized_positions: dict, strategy_name: str, net_worth: float
):
    """
    TODO(david): need to consolidate this func and calculate_rebalance_suggestions
    because `get_rebalancing_suggestions` and `calculate_rebalance_suggestions are confusing
    """
    rebalance_strategy_obj = _get_rebalancing_strategy(strategy_name)
    suggestions = []
    for category, single_category_in_the_portfolio in categorized_positions.items():
        target_sum_of_this_category = (
            net_worth * rebalance_strategy_obj.target_asset_allocation[category]
        )
        investment_shift = (
            single_category_in_the_portfolio["sum"] - target_sum_of_this_category
        ) / net_worth
        suggestions.append(
            {
                "category": category,
                "target_sum_of_this_category": target_sum_of_this_category,
                "investment_shift_of_this_category": investment_shift,
                "sum_of_this_category_in_the_portfolio": single_category_in_the_portfolio[
                    "sum"
                ],
                "suggestions_for_positions": rebalance_strategy_obj.calculate_rebalance_suggestions(
                    category, single_category_in_the_portfolio, net_worth
                ),
            }
        )
    return suggestions


def print_rebalancing_suggestions(suggestions: list[tuple], net_worth: float):
    for suggestion_obj in suggestions:
        print(
            f"Current {suggestion_obj['category']}: {suggestion_obj['sum_of_this_category_in_the_portfolio']:.2f}",
            f"Target Sum: {suggestion_obj['target_sum_of_this_category']:.2f}",
            f"Investment Shift: {suggestion_obj['investment_shift_of_this_category']:.2f}, should be lower than 0.05",
            f"Percentage: {suggestion_obj['sum_of_this_category_in_the_portfolio']/net_worth:.2f}",
        )
        for position_obj in suggestion_obj["suggestions_for_positions"]:
            symbol = position_obj["symbol"]
            balanceUSD = position_obj["balanceUSD"]
            diffrence = position_obj["diffrence"]
            sum_of_this_category_in_the_portfolio = suggestion_obj[
                "sum_of_this_category_in_the_portfolio"
            ]
            print(
                f"Suggestion: modify this amount of USD: {diffrence * balanceUSD / sum_of_this_category_in_the_portfolio:.2f} for position {symbol}, current worth: {balanceUSD:.2f}, percentage: {balanceUSD/net_worth:.2f}"
            )
        print("====================")


def _get_rebalancing_strategy(strategy_name: str) -> callable:
    if strategy_name == "permanent_portfolio":
        return PermanentPortfolio()
    elif strategy_name == "all_weather_portfolio":
        return AllWeatherPortfolio()
    raise NotImplementedError(f"Strategy {strategy_name} is not implemented yet")
