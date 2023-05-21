import json
import math
import random
from collections import defaultdict

import cvxpy as cp
import numpy as np
import requests

from rebalance_server.portfolio_config import (
    DEFILLAMA_API_REQUEST_FREQUENCY_RECIPROCAL,
    ZAPPER_SYMBOL_2_COINGECKO_MAPPING,
)
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
        self._target_desired_weights = [0.4, 0.15, 0.075, 0.075, 0.18, 0.03, 0.06, 0.03]
        self.token_set = set(ZAPPER_SYMBOL_2_COINGECKO_MAPPING.values())
        assert len(self.token_set) < 100
        self._market_cap_of_tokens = {}
        if random.randint(0, DEFILLAMA_API_REQUEST_FREQUENCY_RECIPROCAL) == 0:
            print(
                f"Update coingecko's market cap data by (1/{DEFILLAMA_API_REQUEST_FREQUENCY_RECIPROCAL}) chance"
            )
            self._update_market_cap()
        try:
            self._market_cap_of_tokens = json.load(
                open("./rebalance_server/coingecko/market_cap.json", "r")
            )
        except FileNotFoundError:
            self._update_market_cap()

    def _update_market_cap(self):
        market_cap_resp = requests.get(
            f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={','.join(self.token_set)}&order=market_cap_desc&per_page=100&page=1&sparkline=false&price_change_percentage=1h&locale=en"
        )
        if market_cap_resp.status_code != 200:
            print("Failed to get market cap data from coingecko, use the cached one")
            self._market_cap_of_tokens = json.load(
                open("./rebalance_server/market_cap.json", "r")
            )
        else:
            raw_market_cap_data = market_cap_resp.json()
            self._market_cap_of_tokens = {
                token_obj["id"]: token_obj["market_cap"]
                for token_obj in raw_market_cap_data
            }
            self._market_cap_of_tokens["jones-glp"] = 550385259
            self._market_cap_of_tokens["glp"] = 550385259
        print("[TODO]: need to figure out a way to update jones-glp market cap")
        json.dump(
            self._market_cap_of_tokens,
            open("./rebalance_server/coingecko/market_cap.json", "w"),
        )

    @property
    def target_asset_allocation(self):
        return self._target_asset_allocation

    @property
    def market_cap_of_tokens(self):
        return self._market_cap_of_tokens

    @property
    def category_desired_weights(self):
        return self._target_desired_weights

    def calculate_rebalancing_suggestions(self, categorized_positions, net_worth):
        desired_weights = []
        desired_weights_dict = {}
        index = 0
        lp_pairs_categories = [[], [], [], [], [], [], [], []]
        token_symbol_to_index = {}
        for category_index, single_category_in_the_portfolio in enumerate(
            categorized_positions.values()
        ):
            for position_obj in single_category_in_the_portfolio["portfolio"].values():
                # edge case for Radiant-ETH-lending
                if position_obj["metadata"]["symbol"].lower() == "lending":
                    continue
                # edge case for glp
                if position_obj["metadata"]["symbol"].lower() == "glp":
                    if "glp" not in token_symbol_to_index:
                        token_symbol_to_index["glp"] = index
                        index += 1
                    desired_weights_dict["glp"] = {
                        "index": token_symbol_to_index["glp"],
                        "market_cap": self.market_cap_of_tokens["glp"],
                    }
                    lp_pairs_categories[category_index].append(
                        [token_symbol_to_index["glp"]]
                    )
                    continue
                indices_of_lp_tokens = []
                for token_metadata in position_obj["tokens_metadata"]:
                    mapped_token_symbol = ZAPPER_SYMBOL_2_COINGECKO_MAPPING[
                        token_metadata["symbol"]
                    ]
                    if mapped_token_symbol not in token_symbol_to_index:
                        token_symbol_to_index[mapped_token_symbol] = index
                        index += 1
                    market_cap_of_token = self.market_cap_of_tokens[mapped_token_symbol]
                    desired_weights_dict[mapped_token_symbol] = {
                        "index": token_symbol_to_index[mapped_token_symbol],
                        "market_cap": market_cap_of_token,
                    }
                    indices_of_lp_tokens.append(
                        token_symbol_to_index[mapped_token_symbol]
                    )
                # Define the LP pairs and their categories
                # For example: Tokens 0-1 and 2-3 form LP pairs in the first category, and tokens 4-5 and 6-7 form LP pairs in the second category
                # lp_pairs_categories = [[[0, 1], [2, 3]], [[4, 5], [6, 7]]]
                lp_pairs_categories[category_index].append(indices_of_lp_tokens)
        print("indices_of_lp_tokens: ", lp_pairs_categories)
        # Define the desired weights (market cap weights scaled by All Weather portfolio allocations)
        desired_weights = np.array(
            [
                math.log(token_metadata["market_cap"])
                for token_metadata in sorted(
                    desired_weights_dict.values(), key=lambda x: x["index"]
                )
            ]
        )
        # desired_weights = np.array([token_metadata['market_cap'] for token_metadata in sorted(desired_weights_dict.values(), key=lambda x: x['index'])])

        # Normalize desired_weights
        desired_weights = desired_weights / np.sum(desired_weights)

        # Create a variable for each LP's weight
        lp_weights = cp.Variable(num_pairs)

        # Set up the objective function: minimize the sum of squared differences between desired and actual weights
        objective = cp.Minimize(cp.sum_squares(desired_weights - weights))

        # Set up the constraints: the sum of the weights of the LP pairs in each category equals the category weight,
        # each LP token pair has equal weights for the two tokens, and all weights are non-negative
        # TODO(david): len(lp_pairs_category) == 2 is because GLP and crvCVX are not classic LP token or no LP token.
        print("category_desired_weights: ", self.category_desired_weights)
        constraints = [
            cp.sum([weights[lp_pair] for lp_pair in lp_pairs_category])
            == category_weight
            for lp_pairs_category, category_weight in zip(
                lp_pairs_categories, self.category_desired_weights
            )
            if len(lp_pairs_category) == 2
        ]
        for lp_pairs_category in lp_pairs_categories:
            for lp_pair in lp_pairs_category:
                print(lp_pair)
        # constraints += [weights[lp_pair[0]] == weights[lp_pair[1]] for lp_pairs_category in lp_pairs_categories for lp_pair in lp_pairs_category]
        constraints += [weights >= 0]

        # Define and solve the problem
        problem = cp.Problem(objective, constraints)
        problem.solve()

        # The optimal weights are stored in the 'weights.value' attribute
        optimal_weights = weights.value

        # Normalize optimal_weights
        optimal_weights = optimal_weights / np.sum(optimal_weights)

        # Print the optimal weights
        print("optimal_weights: ", optimal_weights)
        print("==========================")
        print(token_symbol_to_index)
        print("==========================")
        print("==========================")
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

    def get_suggestions_for_positions(
        self, category, _, single_category_in_the_portfolio, net_worth
    ):
        # 6. `symbol.split('-')`
        # 7. calculate how many token you need to sell?
        #     * for sell, just unstake your LP and then swap them to ETH
        #     * for buying, use the investment shift to calculate how many token you need to buy for LP
        # 8. populate those numbers to `zap in` page
        target_sum_of_this_category = net_worth * self.target_asset_allocation[category]
        result = []
        single_category_in_the_portfolio_without_living_expenses = (
            self._delete_special_positions_from_suggestions(
                single_category_in_the_portfolio
            )
        )
        lp_token_name_2_market_cap_proportino_dict = self._calculate_proportion_for_positions_in_a_single_category_by_market_cap_weighting(
            single_category_in_the_portfolio_without_living_expenses
        )

        for (
            symbol,
            position_obj,
        ) in single_category_in_the_portfolio_without_living_expenses[
            "portfolio"
        ].items():
            balanceUSD = position_obj["worth"]
            apr = position_obj["APR"]
            current_ratio_of_this_position_in_this_category = (
                balanceUSD
                / single_category_in_the_portfolio_without_living_expenses["sum"]
            )
            target_ratio_of_this_position_in_this_category = (
                lp_token_name_2_market_cap_proportino_dict[symbol]
            )
            difference = (
                target_sum_of_this_category
                * lp_token_name_2_market_cap_proportino_dict[symbol]
                - single_category_in_the_portfolio_without_living_expenses["sum"]
                * current_ratio_of_this_position_in_this_category
            )
            if (
                abs(
                    target_ratio_of_this_position_in_this_category
                    - current_ratio_of_this_position_in_this_category
                )
                < self.REBALANCE_THRESHOLD
            ) or skip_rebalance_if_position_too_small(abs(difference)):
                difference = 0
            result.append(
                {
                    "symbol": symbol,
                    "balanceUSD": balanceUSD,
                    "apr": apr,
                    "difference": difference,
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

    def _calculate_proportion_for_positions_in_a_single_category_by_market_cap_weighting(
        self, single_category_in_the_portfolio_without_living_expenses: dict
    ) -> dict:
        lp_token_name_2_market_cap_proportino_dict = defaultdict(float)
        for (
            symbol_consists_of_project_and_lp_token,
            position_obj,
        ) in single_category_in_the_portfolio_without_living_expenses[
            "portfolio"
        ].items():
            lp_token_name_2_market_cap_proportino_dict[
                symbol_consists_of_project_and_lp_token
            ] = self._calcualte_market_cap_of_this_lp_token(
                symbol_consists_of_project_and_lp_token, position_obj
            )
        return self._calculate_proportion_via_market_cap_for_all_lp_positions_in_this_category(
            lp_token_name_2_market_cap_proportino_dict
        )

    def _calcualte_market_cap_of_this_lp_token(
        self, symbol_consists_of_project_and_lp_token: str, position_obj: dict
    ) -> float:
        market_cap_of_this_lp_token = 0
        if symbol_consists_of_project_and_lp_token in ["radiant:lending"]:
            return 0
        # average the market cap of all tokens in the LP
        for token_metadata in position_obj["tokens_metadata"]:
            # since most of my LPs are paired with ETH, I don't want to include ETH in the calculation.
            # ETH's market cap is too big, it will skew the result
            if "eth" in token_metadata["symbol"].lower():
                continue
            log_market_cap = math.log(
                self.market_cap_of_tokens[
                    ZAPPER_SYMBOL_2_COINGECKO_MAPPING[token_metadata["symbol"]]
                ]
            )
            composition_of_this_lp_token = position_obj["metadata"]["composition"][
                token_metadata["symbol"].lower()
            ]
            market_cap_of_this_lp_token += log_market_cap * composition_of_this_lp_token
        return self._make_sure_eth_position_would_not_be_skipped(
            market_cap_of_this_lp_token
        )

    @staticmethod
    def _calculate_proportion_via_market_cap_for_all_lp_positions_in_this_category(
        lp_token_name_2_market_cap_proportino_dict: dict,
    ) -> dict:
        sum_of_market_cap = sum(lp_token_name_2_market_cap_proportino_dict.values())
        for (
            symbol_consists_of_project_and_lp_token,
            market_cap,
        ) in lp_token_name_2_market_cap_proportino_dict.items():
            lp_token_name_2_market_cap_proportino_dict[
                symbol_consists_of_project_and_lp_token
            ] = (market_cap / sum_of_market_cap)
        return lp_token_name_2_market_cap_proportino_dict

    def _make_sure_eth_position_would_not_be_skipped(
        self, market_cap_of_this_lp_token: float
    ):
        if market_cap_of_this_lp_token == 0:
            return math.log(
                self.market_cap_of_tokens[ZAPPER_SYMBOL_2_COINGECKO_MAPPING["ETH"]]
            )
        return market_cap_of_this_lp_token
