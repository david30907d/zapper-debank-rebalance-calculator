import json
from collections import defaultdict
import requests
import random
from handlers import get_data_source_handler
from portfolio_config import ADDRESS_2_CATEGORY
def main(defi_portfolio_service_name):
    positions = load_raw_positions(defi_portfolio_service_name)
    categorized_positions = categorize_positions(defi_portfolio_service_name, positions)
    strategy_fn = get_rebalancing_strategy("permanent_portfolio")
    net_worth = output_rebalancing_suggestions(categorized_positions, strategy_fn)
    total_interest = calculate_interest(categorized_positions)
    print(f"Portfolio's APR: {100*total_interest/net_worth:.2f}%")
    print(f"Portfolio's ROI: Unknown")


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
            print(
                f"Suggestion: modify this amount of USD: {diffrence * balanceUSD / portfolio['sum']:.2f} for position {symbol}, current worth: {balanceUSD:.2f}"
            )
            if portfolio['portfolio'][symbol]['APR'] > 0.15:
                print(f"  - Current APR: {portfolio['portfolio'][symbol]['APR']:.2f}, might need to regularly check")

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
            apr = _get_latest_apr(symbol)
            total_interest += position_obj["worth"] * apr
    exrate = _get_exrate("USDTWD")
    print(
        f"Your Annual Interest Rate would be ${total_interest:.2f}, Monthly return in NT$: {total_interest/12*exrate:.0f}"
    )
    return total_interest

def _get_latest_apr(symbol, provider='defillama'):
    if provider == 'defillama':
        defillama_pool_uuid = _get_metadata_by_symbol(symbol).get('defillama-APY-pool-id', None)
        if not defillama_pool_uuid:
            return 0
        res_json = json.load(open('yield-llama.json', 'r'))
        if random.randint(0, 10) == 10:
            res = requests.get('https://yields.llama.fi/pools')
            res_json = res.json()
            json.dump(res_json, open('yield-llama.json', 'w'))
        for pool_metadata in res_json['data']:
            if pool_metadata['pool'] == defillama_pool_uuid:
                # turn APY back to APR
                return ((pool_metadata['apy']/100+1)**(1/365)-1)*365
        raise FileNotFoundError(f"Cannot find {defillama_pool_uuid} in defillama's API")
    else:
        raise NotImplementedError(f"Unknown provider: {provider}")

def _get_metadata_by_symbol(symbol: str) -> dict:
    for metadata in ADDRESS_2_CATEGORY.values():
        if metadata['symbol'] == symbol:
            return metadata
    raise Exception(f"Cannot find {symbol} in your address mapping table")



def _get_exrate(currency_code_name) -> float:
    # credit to https://tw.rter.info/howto_currencyapi.php
    # thanks a lot
    return 30.4
    resp = requests.get("https://tw.rter.info/capi.php")
    currency = resp.json()
    return currency[currency_code_name]["Exrate"]


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
    args = parser.parse_args()
    main(args.defi_portfolio_service_name)

# # basic
# 1. use the same symbol to search in llama response (can use regex to do fozzy search)
# 2. get the max APY
# 3. prompt out for human to check if this protocol is realiable to deposit
# # # advace
# # 1. search other composibilities with higer APY
# # 2. get the max APY
# # 3. prompt out for human to check if this protocol is realiable to deposit
# # 其實這就是在做一個 liquidity pool 的 router, 幫你找到有最佳 APR 的 pool