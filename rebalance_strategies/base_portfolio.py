from abc import ABC

from utils.position import skip_rebalance_if_position_too_small


class BasePortfolio(ABC):
    def __init__(self):
        # target_asset_allocation is just a placeholder, it should be implemented in the subclass
        self.target_asset_allocation = {}

    def calculate_rebalancing_suggestions(self, categorized_positions, net_worth):
        suggestions = []
        for category, single_category_in_the_portfolio in categorized_positions.items():
            target_sum_of_this_category = (
                net_worth * self.target_asset_allocation[category]
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
                    "suggestions_for_positions": self._calculate_suggestions_for_positions(
                        category, single_category_in_the_portfolio, net_worth
                    ),
                }
            )
        return suggestions

    def _calculate_suggestions_for_positions(
        self, category, single_category_in_the_portfolio, net_worth
    ):
        target_sum_of_this_category = net_worth * self.target_asset_allocation[category]
        diffrence = (
            target_sum_of_this_category - single_category_in_the_portfolio["sum"]
        )
        result = []
        for symbol, position_obj in sorted(
            single_category_in_the_portfolio["portfolio"].items(),
            key=lambda x: -x[1]["worth"],
        ):
            balanceUSD = position_obj["worth"]
            if skip_rebalance_if_position_too_small(balanceUSD):
                continue
            result.append(
                {
                    "symbol": symbol,
                    "balanceUSD": balanceUSD,
                    "diffrence": diffrence
                    * balanceUSD
                    / single_category_in_the_portfolio["sum"],
                }
            )
        return result
