import json

ADDRESS_2_CATEGORY = {
    "0x8ec22ec81e740e0f9310e7318d03c494e62a70cd": {
        "categories": ["cash"],
        "symbol": "crvEURSUSD",
    },
    "0xd2d1162512f927a7e282ef43a362659e4f2a728f": {
        "categories": ["gold"],
        "symbol": "glp-avalanche",
    },
    "0xa14dbce13c22c97fd99daa0de3b1b480c7c3fdf6": {
        "categories": ["stock"],
        "symbol": "trader-joe-v2",
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
}


def main():
    positions = _load_raw_positions("zapper")
    categorized_positions = _categorize_positions(positions)
    strategy_fn = _get_rebalancing_strategy("permanent_portfolio")
    _output_rebalancing_suggestions(categorized_positions, strategy_fn)


def _load_raw_positions(source) -> list[dict]:
    return json.load(open("positions.json"))


def _categorize_positions(positions) -> dict:
    """
    user need to label your positions with category type
    """
    result = {
        "gold": {"sum": 0, "portfolio": []},
        "cash": {"sum": 0, "portfolio": []},
        "stock": {"sum": 0, "portfolio": []},
        "bond": {"sum": 0, "portfolio": []},
    }
    for position in positions:
        if position["balanceUSD"] < 200:
            continue
        for product in position["products"]:
            for asset in product["assets"]:
                categories = ADDRESS_2_CATEGORY.get(asset["address"], {}).get(
                    "categories", []
                )
                length_of_categories = len(categories)
                symbol = ADDRESS_2_CATEGORY.get(asset["address"], {}).get("symbol", "")
                for category in categories:
                    weighted_balanceUSD = asset["balanceUSD"] / length_of_categories
                    result[category]["portfolio"].append(
                        {"symbol": symbol, "balanceUSD": weighted_balanceUSD}
                    )
                    result[category]["sum"] += weighted_balanceUSD
    return result

def _get_rebalancing_strategy(strategy_name) -> callable:
    def _permenant_portfolio(_, portfolio, net_worth):
        target_sum = net_worth * 0.25
        diffrence = target_sum - portfolio["sum"]
        sum_of_the_portfolio = sum(position["balanceUSD"] for position in portfolio["portfolio"])
        for position in portfolio['portfolio']:
            print(f"Suggestion: {position['symbol']}, modify this amount of USD: {diffrence * position['balanceUSD'] / sum_of_the_portfolio:.2f}")
            
    if strategy_name == "permanent_portfolio":
        return _permenant_portfolio
    raise NotImplementedError

def _output_rebalancing_suggestions(categorized_positions, strategy_fn):
    net_worth = sum(portfolio["sum"] for portfolio in categorized_positions.values())
    for category, portfolio in categorized_positions.items():
        print(f"Current {category}: {portfolio['sum']:.2f}")
        strategy_fn(category, portfolio, net_worth)
        print('====================')

if __name__ == "__main__":
    main()
