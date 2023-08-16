from collections import defaultdict

import requests

from rebalance_server.apr_utils import convert_apy_to_apr
from rebalance_server.main import load_evm_raw_positions


def get_debank_data():
    # should hard code the contract addresses of vault contracts
    evm_positions = load_evm_raw_positions(
        "debank", "0x0000000000000000000000000000000000000000"
    )
    token_metadata_table: dict[str, dict] = {}
    for position in evm_positions["data"]["result"]["data"]:
        for portfolio_item in position["portfolio_item_list"]:
            for token in portfolio_item["detail"].get(
                "reward_token_list", []
            ) + portfolio_item["detail"].get("supply_token_list", []):
                token_metadata_table[token["id"]] = {
                    "img": token["logo_url"],
                    "price": token["price"],
                    "symbol": token["symbol"],
                    "chain": token["chain"],
                }
    return token_metadata_table


def get_APR_composition(sum_of_APR: float, portfolio_name: str):
    apr_composition = {}
    if portfolio_name == "permanent_portfolio":
        equilibria_market_addrs = {
            "Equilibria-GDAI": "0xa0192f6567f8f5DC38C53323235FD08b318D2dcA",
            "Equilibria-GLP": "0x7D49E5Adc0EAAD9C027857767638613253eF125f",
            "Equilibria-RETH": "0x14FbC760eFaF36781cB0eb3Cb255aD976117B9Bd",
        }
        for key, pool_addr in equilibria_market_addrs.items():
            apr_composition[key] = _fetch_equilibria_APR_composition(pool_addr)
        apr_composition["SushSwap-DpxETH"] = _fetch_sushiswap_APR_composition(
            "0x0c1cf6883efa1b496b01f654e247b9b419873054"
        )
        return apr_composition
    raise NotImplementedError(f"Portfolio {portfolio_name} is not implemented")


def _fetch_equilibria_APR_composition(pool_addr: str) -> float:
    result = defaultdict(lambda: defaultdict(float))
    equilibria_chain_info_map = requests.get("https://equilibria.fi/api/chain-info-map")
    if equilibria_chain_info_map.status_code != 200:
        raise Exception("Failed to fetch equilibria chain info map")
    equilibria_chain_info_map = equilibria_chain_info_map.json()
    result["underlyingAPY"]["token"] = []
    for category, keys in {
        "Swap Fee": ["swapFeeApy"],
        "underlyingAPY": ["underlyingApy", "lpRewardApy"],
        "PENDLE": ["aggregatedApy"],
    }.items():
        for key in keys:
            result[category]["APR"] += convert_apy_to_apr(
                equilibria_chain_info_map["42161"]["marketMap"][pool_addr][key]
            )
        if category == "PENDLE":
            result[category]["token"] = "0x0c880f6761F1af8d9Aa9C466984b80DAb9a8c9e8"
        elif category == "underlyingAPY":
            for reward in equilibria_chain_info_map["42161"]["marketMap"][pool_addr][
                "underlyingRewardApyBreakdown"
            ]:
                result[category]["token"].append(reward["asset"]["address"])
            result[category]["token"].append(
                equilibria_chain_info_map["42161"]["marketMap"][pool_addr][
                    "basePricingAsset"
                ]["address"]
            )
    return result


def _fetch_sushiswap_APR_composition(pool_addr: str) -> float:
    result = defaultdict(lambda: defaultdict(float))
    pool_res = requests.get(f"https://pools.sushi.com/api/v0/42161/{pool_addr}")
    if pool_res.status_code != 200:
        raise Exception("Failed to fetch kava sushiswap APR")
    pool_json = pool_res.json()
    for incentive in pool_json["incentives"]:
        if incentive["apr"] > 0:
            symbol = incentive["rewardToken"]["symbol"]
            result[symbol]["token"] = incentive["rewardToken"]["address"]
            result[symbol]["APR"] = incentive["apr"]

    result["Swap Fee"]["APR"] = pool_json["feeApr1d"]
    return result
