from rebalance_strategies.utils import show_rebalance_suggestions


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
    show_rebalance_suggestions(category, portfolio, net_worth, target_asset_allocation)
