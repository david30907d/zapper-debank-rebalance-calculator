import json
import os
from collections import defaultdict
from pathlib import Path

import requests
from dotenv import load_dotenv

from rebalance_server.apr_utils.apr_calculator import get_lowest_or_default_apr
from rebalance_server.apr_utils.apr_pool_optimizer import (
    print_out_topn_candidate_pool,
    search_better_stable_coin_pools,
    search_top_n_pool_consist_of_same_lp_token,
    show_topn_stable_coins,
)
from rebalance_server.handlers import get_data_source_handler

# TODO(david): uncomment sharpe ratio and max drawdown once we've migrated to standalone server not lambda or cloud run
# from rebalance_server.adapters.networth_to_balance_adapter import (
#     get_networh_to_balance_adapter,
# )
# from rebalance_server.metrics.max_drawdown import calculate_max_drawdown
# from rebalance_server.metrics.sharpe_ratio import calculate_portfolio_sharpe_ratio
from rebalance_server.rebalance_strategies import (
    get_rebalancing_suggestions,
    print_rebalancing_suggestions,
)
from rebalance_server.utils.exchange_rate import get_exrate

dotenv_path = Path("./rebalance_server/.env")
load_dotenv(dotenv_path=dotenv_path)


def main(
    defi_portfolio_service_name: str,
    optimize_apr_mode: str,
    strategy_name: str,
    addresses: list[str],
):
    evm_positions = load_evm_raw_positions(defi_portfolio_service_name, addresses)
    evm_categorized_positions = categorize_positions(
        defi_portfolio_service_name, evm_positions
    )
    # CEX & cosmos posistions
    # 1. Binance
    # 2. Nansen
    # because some of my sizes are located in Binance, and Nansen(cosmos ecosystem), which is not included in either debank or zapper
    # therefore, these 2 data sources need to be loaded everytime (ps. they're all manually updated in debank data format)
    no_evm_posistions = _load_no_evm_posistions(
        data_sources={
            "binance": "debank",
            "nansen-cosmos": "nansen",
            "nansen-osmo": "nansen",
        }
    )
    no_evm_categorized_positions_array = _categorize_no_evm_categorized_positions_array(
        no_evm_posistions
    )
    categorized_positions = _merge_categorized_positions(
        evm_categorized_positions, no_evm_categorized_positions_array
    )
    net_worth = _get_networth(categorized_positions)
    suggestions = get_rebalancing_suggestions(
        categorized_positions, strategy_name, net_worth
    )
    print_rebalancing_suggestions(suggestions, net_worth)
    print(f"Current Net Worth: ${net_worth:.2f}")
    total_interest = calculate_interest(categorized_positions)
    portfolio_apr = 100 * total_interest / net_worth
    print(f"Portfolio's APR: {portfolio_apr:.2f}%")

    # [TODO](david): uncomment sharpe ratio and max drawdown once we've migrated to standalone server not lambda or cloud run
    # adapter = get_networh_to_balance_adapter(adapter="coingecko")
    # categorized_positions_with_token_balance = adapter(categorized_positions)

    # since some alpha tokens only have few data points, making the data very less. In other words, sharpe ratio is not reliable at this point until those alpha tokens has a few years worth of data
    # sharpe_ratio = calculate_portfolio_sharpe_ratio(
    #     categorized_positions_with_token_balance
    # )
    # print(
    #     f"Portfolio's Sharpe Ratio (Useless until we have enough data points): {sharpe_ratio:.2f}"
    # )
    # print(
    #     f"Portfolio's Max Drawdown: {calculate_max_drawdown(categorized_positions_with_token_balance):.2f}"
    # )
    if optimize_apr_mode:
        top_n_with_metadata = search_top_n_pool_consist_of_same_lp_token(
            categorized_positions, optimize_apr_mode
        )
        for project_symbol, top_n, apr in top_n_with_metadata:
            print_out_topn_candidate_pool(project_symbol, top_n, apr)
        topn_stable_coins = search_better_stable_coin_pools(categorized_positions)
        show_topn_stable_coins(topn_stable_coins)
    return {
        "suggestions": suggestions,
        "total_interest": total_interest,
        "portfolio_apr": portfolio_apr,
        # TODO(david): uncomment sharpe ratio and max drawdown once we've migrated to standalone server not lambda or cloud run
        # "sharpe_ratio": sharpe_ratio,
        "top_n_pool_consist_of_same_lp_token": top_n_with_metadata,
        "topn_stable_coins": topn_stable_coins,
    }


def load_raw_positions(data_format: str) -> dict:
    return json.load(open(f"./rebalance_server/dashboard/{data_format}.json"))


def load_evm_raw_positions(data_format: str, addresses: list[str]) -> dict:
    if os.getenv("DEBUG", "").lower() == "true":
        return json.load(open(f"./rebalance_server/dashboard/{data_format}.json"))
    merged_data = []
    for address in addresses:
        data = requests.get(
            f"https://pro-openapi.debank.com/v1/user/all_complex_protocol_list?id={address}",
            headers={"AccessKey": os.getenv("ACCESSKEY")},
        ).json()
        merged_data += data
    return {"data": {"result": {"data": merged_data}}}


def categorize_positions(defi_portfolio_service_name, positions) -> dict:
    """
    user need to label your positions with category type
    """
    result = {
        "long_term_bond": {
            "sum": 0,
            "portfolio": defaultdict(lambda: defaultdict(int)),
        },
        "intermediate_term_bond": {
            "sum": 0,
            "portfolio": defaultdict(lambda: defaultdict(int)),
        },
        "commodities": {"sum": 0, "portfolio": defaultdict(lambda: defaultdict(int))},
        "gold": {"sum": 0, "portfolio": defaultdict(lambda: defaultdict(int))},
        "large_cap_us_stocks": {
            "sum": 0,
            "portfolio": defaultdict(lambda: defaultdict(int)),
        },
        "small_cap_us_stocks": {
            "sum": 0,
            "portfolio": defaultdict(lambda: defaultdict(int)),
        },
        "non_us_developed_market_stocks": {
            "sum": 0,
            "portfolio": defaultdict(lambda: defaultdict(int)),
        },
        "non_us_emerging_market_stocks": {
            "sum": 0,
            "portfolio": defaultdict(lambda: defaultdict(int)),
        },
    }
    handler = get_data_source_handler(defi_portfolio_service_name)
    return handler(positions, result)


def calculate_interest(categorized_positions):
    interest_rank_list = defaultdict(float)
    total_interest = 0
    for portfolio in categorized_positions.values():
        for project_symbol, position_obj in portfolio["portfolio"].items():
            apr = get_lowest_or_default_apr(
                project_symbol, position_obj["metadata"].get("defillama-APY-pool-id")
            )
            interest_rank_list[project_symbol] += position_obj["worth"] * apr
            total_interest += position_obj["worth"] * apr
    exrate = get_exrate("USDTWD")
    print(
        f"Your Annual Interest Rate would be ${total_interest:.2f}, Monthly return in NT$: {total_interest/12*exrate:.0f}"
    )
    print("\nTop 5 Revenue Farm this Month:")
    for pool, interest in sorted(interest_rank_list.items(), key=lambda x: -x[1])[:5]:
        print(f"{pool}: ${interest/12:.2f}")
    return total_interest


def _load_no_evm_posistions(data_sources: dict) -> list[dict]:
    result = []
    for data_source, handler in data_sources.items():
        result.append((load_raw_positions(data_source), handler))
    return result


def _categorize_no_evm_categorized_positions_array(
    no_evm_posistions: list[dict],
) -> list[dict]:
    no_evm_categorized_positions_array = []
    for no_evm_posistion, handler in no_evm_posistions:
        no_evm_categorized_position = categorize_positions(
            defi_portfolio_service_name=handler, positions=no_evm_posistion
        )
        no_evm_categorized_positions_array.append(no_evm_categorized_position)
    return no_evm_categorized_positions_array


def _get_networth(categorized_positions: dict):
    return sum(portfolio["sum"] for portfolio in categorized_positions.values())


def _merge_categorized_positions(
    evm_categorized_positions: dict, no_evm_categorized_positions_array: list[dict]
) -> dict:
    result = evm_categorized_positions
    for no_evm_categorized_positions in no_evm_categorized_positions_array:
        for category, portfolio_metadata in no_evm_categorized_positions.items():
            result[category]["sum"] += portfolio_metadata["sum"]
            result[category]["portfolio"] = {
                **evm_categorized_positions[category]["portfolio"],
                **portfolio_metadata["portfolio"],
            }
    return result


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--defi_portfolio_service_name",
        type=str,
        choices=["zapper", "debank"],
        help="which defi portfolio to load positions from",
    )
    parser.add_argument(
        "-op",
        "--optimize_apr_mode",
        type=str,
        choices=["new_pool", "new_combination"],
        help="which defi portfolio to load positions from",
    )
    parser.add_argument(
        "-st",
        "--strategy_name",
        type=str,
        choices=["permanent_portfolio", "all_weather_portfolio"],
        help="which target asset allocation to use",
    )
    args = parser.parse_args()
    main(args.defi_portfolio_service_name, args.optimize_apr_mode, args.strategy_name)
