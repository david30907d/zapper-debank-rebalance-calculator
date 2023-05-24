from rebalance_server.rebalance_strategies.base_portfolio import BasePortfolio
from rebalance_server.utils.position import skip_rebalance_if_position_too_small


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

    def get_suggestions_for_positions(
        self, category, investment_shift, single_category_in_the_portfolio, net_worth
    ):
        # if abs(investment_shift) < self.REBALANCE_THRESHOLD:
        #     return []
        target_sum_of_this_category = net_worth * self.target_asset_allocation[category]
        result = []
        single_category_in_the_portfolio_without_living_expenses = (
            self._delete_special_positions_from_suggestions(
                single_category_in_the_portfolio
            )
        )
        for (
            symbol,
            position_obj,
        ) in single_category_in_the_portfolio_without_living_expenses[
            "portfolio"
        ].items():
            balanceUSD = position_obj["worth"]
            apr = position_obj["APR"]
            difference = (
                (
                    target_sum_of_this_category
                    - single_category_in_the_portfolio_without_living_expenses["sum"]
                )
                * balanceUSD
                / single_category_in_the_portfolio["sum"]
            )
            if skip_rebalance_if_position_too_small(abs(difference)):
                difference = 0
            result.append(
                {
                    "symbol": symbol,
                    "balanceUSD": balanceUSD,
                    "apr": apr,
                    "difference": difference,
                    "metadata": position_obj["metadata"],
                    "for_dex": {
                        token: difference * percentage
                        for token, percentage in position_obj["metadata"][
                            "composition"
                        ].items()
                    }
                    if "glp" not in symbol.lower()
                    else {"glp": difference},
                }
            )
        return result

    @staticmethod
    def _delete_special_positions_from_suggestions(
        single_category_in_the_portfolio: dict,
    ) -> dict:
        # 1. no suggestions for user's living expenses
        # since it varies from person to person
        # 2. no suggestions for airdrop tokens
        symbols_to_delete = []

        for symbol, position_obj in single_category_in_the_portfolio[
            "portfolio"
        ].items():
            if (
                position_obj["metadata"].get("living-expenses") is True
                or position_obj["metadata"].get("forAirdrop") is True
            ):
                symbols_to_delete.append(symbol)

        for symbol in symbols_to_delete:
            del single_category_in_the_portfolio["portfolio"][symbol]
        return single_category_in_the_portfolio
