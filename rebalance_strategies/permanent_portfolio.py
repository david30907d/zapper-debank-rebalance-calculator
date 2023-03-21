from rebalance_strategies.utils import show_rebalance_suggestions


def permenant_portfolio(category, portfolio, net_worth):
    """
    stock total allocation should be 25%
    Apply all weather portfolio's allocation for large_cap_us_stocks, small_cap_us_stocks, non_us_developed_market_stocks, non_us_emerging_market_stocks these 4 categories
    """
    target_asset_allocation = {
        "long_term_bond": 0.25,
        "intermediate_term_bond": 0.25,
        "commodities": 0,
        "gold": 0.25,
        "large_cap_us_stocks": 0.15,
        "small_cap_us_stocks": 0.025,
        "non_us_developed_market_stocks": 0.05,
        "non_us_emerging_market_stocks": 0.025,
    }
    show_rebalance_suggestions(category, portfolio, net_worth, target_asset_allocation)
