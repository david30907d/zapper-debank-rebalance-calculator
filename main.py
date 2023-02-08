import json
from collections import defaultdict
ZAPPER_ADDRESS = {
        "0x8ec22ec81e740e0f9310e7318d03c494e62a70cd": {
            "categories": ["cash"],
            "symbol": "crvEURSUSD",
        },
        "0xd2d1162512f927a7e282ef43a362659e4f2a728f": {
            "categories": ["gold"],
            "symbol": "glp-avax",
        },
        "0xa14dbce13c22c97fd99daa0de3b1b480c7c3fdf6": {
            "categories": ["stock"],
            "symbol": "trader-joe-dpx-weth",
        },
        "0xf4d73326c13a4fc5fd7a064217e12780e9bd62c3": {
            "categories": ["stock"],
            "symbol": "magic",
        },
        "0x4e971a87900b931ff39d1aad67697f49835400b6": {
            "categories": ["gold"],
            "symbol": "glp-arbitrum",
        },
        "0x100ec08129e0fd59959df93a8b914944a3bbd5df": {
            "categories": ["bond"],
            "symbol": "vesta-finance",
        },
        "0x127963a74c07f72d862f2bdc225226c3251bd117": {
            "categories": ["cash"],
            "symbol": "VSTFRAX-f",
        },
        "0x27a8c58e3de84280826d615d80ddb33930383fe9": {
            "categories": ["cash", "bond", "gold"],
            "symbol": "cvxOHMFRAXBP-f",
        },
        "0x72a19342e8f1838460ebfccef09f6585e32db86e": {
            "categories": ["stock"],
            "symbol": "CVX",
        },
        "0xaa0c3f5f7dfd688c6e646f66cd2a6b66acdbe434": {
            "categories": ["stock"],
            "symbol": "cvxCRV",
        },
        "0x188bed1968b795d5c9022f6a0bb5931ac4c18f00": {
            "categories": ["stock"],
            "symbol": "Yeti-JLP",
        },
        "0xf562b2f33b3c90d5d273f88cdf0ced866e17092e": {
            "categories": ["bond", "cash", "gold"],
            "symbol": "FraxSwapOHM",
        },
        "0xf650c3d88d12db855b8bf7d11be6c55a4e07dcc9": {
            "categories": ["cash"],
            "symbol": "compund USDT",
        },
        "0x8d9ba570d6cb60c7e3e0f31343efe75ab8e65fb1": {
            "categories": ["bond"],
            "symbol": "gohm-arb"
        },
        "0x0ab87046fbb341d058f17cbc4c1133f25a20a52f": {
            "categories": ["bond"],
            "symbol": "gohm"
        },
        "0x1f80c96ca521d7247a818a09b0b15c38e3e58a28": {
            # TODO: david to figure out weather dpx is stock or gold
            "categories": ["stock"],
            "symbol": "sushi-dpx-weth-LP"
        },
        "0x1701a7e5034ed1e35c52245ab7c07dbdaf353de7": {
            "categories": ["stock"],
            "symbol": "kyber-avax-eth-LP"
        }
}
DEBANK_ADDRESS = {
        "0xfffffffffff5d3627294fec5081ce5c5d7fa6451": {
            "categories": ["cash",],
            "symbol": "YUSD",
        },
        "0xb5352a39c11a81fe6748993d586ec448a01f08b5": {
            "categories": ["cash", "stock", "gold"],
            "symbol": "avax-usdc-TJ-avax"
        },
        "0xc963ef7d977ecb0ab71d835c4cb1bf737f28d010": {
            "categories": ["stock"],
            "symbol": "radiant-eth-LP"
        },
        "0xb7e50106a5bd3cf21af210a755f9c8740890a8c9": {
            "categories": ["stock"],
            "symbol": "magic-weth-sushi-LP"
        },
        "0x7ec3717f70894f6d9ba0be00774610394ce006ee": {
            "categories": ["stock", "gold", "cash"],
            "symbol": "weth-usdc-TJ-LP"
        },
        "0x5fbbef48ce0850e5a73bc3f4a6e903458b3c0af4": {
            "categories": ["stock", "gold"],
            "symbol": "weth-gmx-TJ-LP-arb"
        },
        "0x42be75636374dfa0e57eb96fa7f68fe7fcdad8a3": {
            "categories": ["stock"],
            "symbol": "weth-avax-TJ-LP-avax"
        },
        "0xdf3e481a05f58c387af16867e9f5db7f931113c9": {
            "categories": ["stock", "cash", "gold"],
            "symbol": "weth-usdt-TJ-LP-avax"
        },
        "0x104f1459a2ffea528121759b238bb609034c2f01" : {
            "categories": ["stock", "cash", "gold"],
            "symbol": "balancer-usdt-eth-btc-arb"
        },
        "0x3d9819210a31b4961b30ef54be2aed79b9c9cd3b": {
            "categories": ["cash"],
            "symbol": "compound USDT"
        },
        "0x5851e2d6396bcc26fb9eee21effbf99e0d2b2148": {
            "categories": ["stock", "cash", "gold"],
            "symbol": "weth-usdc-TJ-LP-avax"
        }
    }

ADDRESS_2_CATEGORY = {**ZAPPER_ADDRESS, **DEBANK_ADDRESS}
def main(defi_portfolio_service_name):
    positions = _load_raw_positions(defi_portfolio_service_name)
    categorized_positions = _categorize_positions(
        defi_portfolio_service_name, positions
    )
    strategy_fn = _get_rebalancing_strategy("permanent_portfolio")
    _output_rebalancing_suggestions(categorized_positions, strategy_fn)


def _load_raw_positions(data_format: str) -> list[dict]:
    return json.load(open(f"{data_format}.json"))


def _categorize_positions(defi_portfolio_service_name, positions) -> dict:
    """
    user need to label your positions with category type
    """
    result = {
        "gold": {"sum": 0, "portfolio": defaultdict(int)},
        "cash": {"sum": 0, "portfolio": defaultdict(int)},
        "stock": {"sum": 0, "portfolio": defaultdict(int)},
        "bond": {"sum": 0, "portfolio": defaultdict(int)},
    }
    handler = _get_data_source_handler(defi_portfolio_service_name)
    return handler(positions, result)


def _get_data_source_handler(defi_portfolio_service_name) -> callable:
    if defi_portfolio_service_name == "zapper":
        return _zapper_handler
    elif defi_portfolio_service_name == "debank":
        return _debank_handler
    raise NotImplementedError


def _zapper_handler(positions, result):
    for position in positions:
        if position["balanceUSD"] < 200:
            continue
        for product in position["products"]:
            for asset in product["assets"]:
                asset_address = asset["address"] if not asset.get("dataProps", {}).get("poolAddress") else asset.get("dataProps", {}).get("poolAddress")
                categories = ADDRESS_2_CATEGORY.get(asset_address, {}).get(
                    "categories", []
                )
                # my sentry logic
                if asset["balanceUSD"] > 200 and not categories:
                    print(json.dumps(asset))
                    raise Exception("no category, need to update your ADDRESS_2_CATEGORY")
                length_of_categories = len(categories)
                symbol = ADDRESS_2_CATEGORY.get(asset["address"], {}).get("symbol", "")
                for category in categories:
                    weighted_balanceUSD = asset["balanceUSD"] / length_of_categories
                    result[category]["portfolio"][symbol] += weighted_balanceUSD
                    result[category]["sum"] += weighted_balanceUSD
    return result


def _debank_handler(positions, result):
    def _get_correct_addr(portfolio):
        addr = portfolio['pool']['id'] if len(portfolio['pool']['id'].split(':')) == 1 else portfolio['pool']['id'].split(':')[1]
        if len(addr) != 42:
            # TODO: use a function to handle
            addr = portfolio['pool']['controller']
        return addr
    for pool in positions["data"]["result"]["data"]:
        for portfolio in pool['portfolio_item_list']:
            addr = _get_correct_addr(portfolio)
            categories = ADDRESS_2_CATEGORY.get(addr, {}).get(
                "categories", []
            )
            # my sentry logic
            if portfolio['stats']["net_usd_value"] > 200 and not categories:
                print(json.dumps(portfolio))
                raise Exception("no category, need to update your ADDRESS_2_CATEGORY")
            length_of_categories = len(categories)
            symbol = ADDRESS_2_CATEGORY.get(addr, {}).get("symbol", "")
            for category in categories:
                weighted_balanceUSD = portfolio['stats']["net_usd_value"] / length_of_categories
                result[category]["portfolio"][symbol] += weighted_balanceUSD
                result[category]["sum"] += weighted_balanceUSD
    return result
                        

def _get_rebalancing_strategy(strategy_name) -> callable:
    def _permenant_portfolio(category, portfolio, net_worth):
        target_sum = net_worth * 0.25
        print(f"Current {category}: {portfolio['sum']:.2f}", f"Target Sum: {target_sum:.2f}", f"Investment Shift: {(portfolio['sum']-target_sum)/net_worth:.2f}, should be lower than 0.05")
        diffrence = target_sum - portfolio["sum"]
        for symbol, balanceUSD in sorted(portfolio["portfolio"].items(), key=lambda x: -x[1]):
            print(
                f"Suggestion: modify this amount of USD: {diffrence * balanceUSD / portfolio['sum']:.2f} for position {symbol}, current worth: {balanceUSD:.2f}"
            )

    if strategy_name == "permanent_portfolio":
        return _permenant_portfolio
    raise NotImplementedError


def _output_rebalancing_suggestions(categorized_positions, strategy_fn):
    net_worth = sum(portfolio["sum"] for portfolio in categorized_positions.values())
    for category, portfolio in categorized_positions.items():
        strategy_fn(category, portfolio, net_worth)
        print("====================")
    print(f"Current Net Worth: ${net_worth:.2f}")


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
