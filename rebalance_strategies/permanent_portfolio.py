from rebalance_server.rebalance_strategies.base_portfolio import BasePortfolio
from rebalance_server.utils.position import skip_rebalance_if_position_too_small


class PermanentPortfolio(BasePortfolio):
    """
    stock total allocation should be 25%
    Apply all weather portfolio's allocation for large_cap_us_stocks, small_cap_us_stocks, non_us_developed_market_stocks, non_us_emerging_market_stocks these 4 categories
    """

    def __init__(self):
        self._target_asset_allocation = {
            "long_term_bond": 0.25,
            "intermediate_term_bond": 0.25,
            "commodities": 0,
            "gold": 0.25,
            "large_cap_us_stocks": 0.15,
            "small_cap_us_stocks": 0.025,
            "non_us_developed_market_stocks": 0.05,
            "non_us_emerging_market_stocks": 0.025,
        }

    @property
    def target_asset_allocation(self):
        return self._target_asset_allocation

    def get_suggestions_for_positions(
        self, category, investment_shift, single_category_in_the_portfolio, net_worth
    ):
        if abs(investment_shift) < self.REBALANCE_THRESHOLD:
            return []
        target_sum_of_this_category = net_worth * self.target_asset_allocation[category]
        difference = (
            target_sum_of_this_category - single_category_in_the_portfolio["sum"]
        )
        result = []
        for symbol, position_obj in sorted(
            single_category_in_the_portfolio["portfolio"].items(),
            key=lambda x: -x[1]["worth"],
        ):
            balanceUSD = position_obj["worth"]
            apr = position_obj["APR"]
            if skip_rebalance_if_position_too_small(balanceUSD):
                continue
            result.append(
                {
                    "symbol": symbol,
                    "balanceUSD": balanceUSD,
                    "apr": apr,
                    "difference": difference
                    * balanceUSD
                    / single_category_in_the_portfolio["sum"],
                }
            )
        return result
