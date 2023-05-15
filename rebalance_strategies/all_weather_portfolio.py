import json
import math
import random
from collections import defaultdict

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

    def get_suggestions_for_positions(
        self, category, investment_shift, single_category_in_the_portfolio, net_worth
    ):
        # 6. `symbol.split('-')`
        # 7. calculate how many token you need to sell?
        #     * for sell, just unstake your LP and then swap them to ETH
        #     * for buying, use the investment shift to calculate how many token you need to buy for LP
        # 8. populate those numbers to `zap in` page

        target_sum_of_this_category = net_worth * self.target_asset_allocation[category]
        result = []
        lp_token_name_2_market_cap_proportino_dict = self._calculate_proportion_for_positions_in_a_single_category_by_market_cap_weighting(
            single_category_in_the_portfolio
        )

        for symbol, position_obj in single_category_in_the_portfolio[
            "portfolio"
        ].items():
            balanceUSD = position_obj["worth"]
            apr = position_obj["APR"]
            current_ratio_of_this_position_in_this_category = (
                balanceUSD / single_category_in_the_portfolio["sum"]
            )
            target_ratio_of_this_position_in_this_category = (
                lp_token_name_2_market_cap_proportino_dict[symbol]
            )
            difference = (
                target_sum_of_this_category
                * lp_token_name_2_market_cap_proportino_dict[symbol]
                - single_category_in_the_portfolio["sum"]
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

    def _calculate_proportion_for_positions_in_a_single_category_by_market_cap_weighting(
        self, single_category_in_the_portfolio: dict
    ) -> dict:
        lp_token_name_2_market_cap_proportino_dict = defaultdict(float)
        for (
            symbol_consists_of_project_and_lp_token,
            position_obj,
        ) in single_category_in_the_portfolio["portfolio"].items():
            print(symbol_consists_of_project_and_lp_token)
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
        print(position_obj["metadata"]["composition"])
        # average the market cap of all tokens in the LP
        for token_metadata in position_obj["tokens_metadata"]:
            # since most of my LPs are paired with ETH, I don't want to include ETH in the calculation.
            # ETH's market cap is too big, it will skew the result
            if "eth" in token_metadata["symbol"].lower():
                continue
            print(
                token_metadata,
                token_metadata["symbol"] in position_obj["metadata"]["composition"],
            )
            log_market_cap = math.log(
                self.market_cap_of_tokens[
                    ZAPPER_SYMBOL_2_COINGECKO_MAPPING[token_metadata["symbol"]]
                ]
            )
            composition_of_this_lp_token = position_obj["metadata"]["composition"][
                token_metadata["symbol"].lower()
            ]
            # market_cap_of_this_lp_token += log_market_cap * composition_of_this_lp_token
            market_cap_of_this_lp_token += log_market_cap * composition_of_this_lp_token
        # market_cap_of_this_lp_token /= len(
        #     position_obj["tokens_metadata"]
        # )
        return self._make_sure_eth_position_would_not_be_skipped(
            market_cap_of_this_lp_token
        )
        # lp_token_name_2_market_cap_proportino_dict[symbol_consists_of_project_and_lp_token] = self._make_sure_eth_position_would_not_be_skipped(lp_token_name_2_market_cap_proportino_dict[symbol_consists_of_project_and_lp_token])
        return market_cap_of_this_lp_token

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
