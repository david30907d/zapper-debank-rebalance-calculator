from rebalance_strategies.base_portfolio import BasePortfolio


class AllWeatherPortfolio(BasePortfolio):
    """
    these propotions are from ray dalio's book
    """

    def __init__(self):
        self._target_asset_allocation = {
            "long_term_bond": 0.4,
            "intermediate_term_bond": 0.15,
            "commodities": 0.075,
            "gold": 0.075,
            "large_cap_us_stocks": 0.18,
            "small_cap_us_stocks": 0.03,
            "non_us_developed_market_stocks": 0.06,
            "non_us_emerging_market_stocks": 0.03,
        }

    @property
    def target_asset_allocation(self):
        return self._target_asset_allocation
