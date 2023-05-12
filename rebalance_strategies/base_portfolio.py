from abc import ABC, abstractmethod


class BasePortfolio(ABC):
    REBALANCE_THRESHOLD = 0.05

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
            suggestions_for_this_category = self._get_suggestions_for_this_category(
                category,
                target_sum_of_this_category,
                investment_shift,
                single_category_in_the_portfolio,
                net_worth,
            )
            suggestions.append(suggestions_for_this_category)
        return suggestions

    def _get_suggestions_for_this_category(
        self,
        category,
        target_sum_of_this_category,
        investment_shift,
        single_category_in_the_portfolio,
        net_worth,
    ):
        return {
            "category": category,
            "target_sum_of_this_category": target_sum_of_this_category,
            "investment_shift_of_this_category": investment_shift,
            "sum_of_this_category_in_the_portfolio": single_category_in_the_portfolio[
                "sum"
            ],
            "suggestions_for_positions": self.get_suggestions_for_positions(
                category, investment_shift, single_category_in_the_portfolio, net_worth
            ),
        }

    @abstractmethod
    def get_suggestions_for_positions(self):
        pass
