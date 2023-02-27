import json
from collections import defaultdict

from apr_utils.apr_calculator import get_latest_apr
from apr_utils.apr_pool_optimizer import search_top_n_pool_consist_of_same_lp_token
from handlers import get_data_source_handler
from metrics.max_drawdown import calculate_max_drawdown
from metrics.sharpe_ratio import calculate_portfolio_sharpe_ratio
from utils.exchange_rate import get_exrate
from utils.position import skip_rebalance_if_position_too_small


def main(defi_portfolio_service_name: str, optimize_apr_mode: str):
    positions = load_raw_positions(defi_portfolio_service_name)
    categorized_positions = categorize_positions(defi_portfolio_service_name, positions)
    strategy_fn = get_rebalancing_strategy("permanent_portfolio")
    net_worth = output_rebalancing_suggestions(categorized_positions, strategy_fn)
    total_interest = calculate_interest(categorized_positions)
    print(f"Portfolio's APR: {100*total_interest/net_worth:.2f}%")
    print("Portfolio's ROI: Unknown\n")
    print(
        "Portfolio's Sharpe Ratio: ",
        calculate_portfolio_sharpe_ratio(
            {
                "governance-ohm": 10,
            }
        ),
    )
    print(
        "Portfolio's Max Drawdown: ",
        calculate_max_drawdown(
            {
                "governance-ohm": 10,
            }
        ),
    )
    if optimize_apr_mode:
        search_top_n_pool_consist_of_same_lp_token(
            categorized_positions, optimize_apr_mode
        )


def load_raw_positions(data_format: str) -> list[dict]:
    return json.load(open(f"{data_format}.json"))


def categorize_positions(defi_portfolio_service_name, positions) -> dict:
    """
    user need to label your positions with category type
    """
    result = {
        "gold": {"sum": 0, "portfolio": defaultdict(lambda: defaultdict(int))},
        "cash": {"sum": 0, "portfolio": defaultdict(lambda: defaultdict(int))},
        "stock": {"sum": 0, "portfolio": defaultdict(lambda: defaultdict(int))},
        "bond": {"sum": 0, "portfolio": defaultdict(lambda: defaultdict(int))},
    }
    handler = get_data_source_handler(defi_portfolio_service_name)
    return handler(positions, result)


def get_rebalancing_strategy(strategy_name) -> callable:
    def _permenant_portfolio(category, portfolio, net_worth):
        target_sum = net_worth * 0.25
        print(
            f"Current {category}: {portfolio['sum']:.2f}",
            f"Target Sum: {target_sum:.2f}",
            f"Investment Shift: {(portfolio['sum']-target_sum)/net_worth:.2f}, should be lower than 0.05",
        )
        diffrence = target_sum - portfolio["sum"]
        for symbol, position_obj in sorted(
            portfolio["portfolio"].items(), key=lambda x: -x[1]["worth"]
        ):
            balanceUSD = position_obj["worth"]
            if skip_rebalance_if_position_too_small(balanceUSD):
                continue
            print(
                f"Suggestion: modify this amount of USD: {diffrence * balanceUSD / portfolio['sum']:.2f} for position {symbol}, current worth: {balanceUSD:.2f}"
            )

    if strategy_name == "permanent_portfolio":
        return _permenant_portfolio
    raise NotImplementedError


def output_rebalancing_suggestions(categorized_positions, strategy_fn):
    net_worth = sum(portfolio["sum"] for portfolio in categorized_positions.values())
    for category, portfolio in categorized_positions.items():
        strategy_fn(category, portfolio, net_worth)
        print("====================")
    print(f"Current Net Worth: ${net_worth:.2f}")
    return net_worth


def calculate_interest(categorized_positions):
    total_interest = 0
    for portfolio in categorized_positions.values():
        for symbol, position_obj in portfolio["portfolio"].items():
            apr = get_latest_apr(symbol)
            total_interest += position_obj["worth"] * apr
    exrate = get_exrate("USDTWD")
    print(
        f"Your Annual Interest Rate would be ${total_interest:.2f}, Monthly return in NT$: {total_interest/12*exrate:.0f}"
    )
    return total_interest


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
    args = parser.parse_args()
    main(args.defi_portfolio_service_name, args.optimize_apr_mode)

# # basic
# 1. use the same symbol to search in llama response (can use regex to do fozzy search)
# 2. get the max APY
# 3. prompt out for human to check if this protocol is realiable to deposit
# # # advace
# # 1. search other composibilities with higer APY
# # 2. get the max APY
# # 3. prompt out for human to check if this protocol is realiable to deposit
# # 其實這就是在做一個 liquidity pool 的 router, 幫你找到有最佳 APR 的 pool
