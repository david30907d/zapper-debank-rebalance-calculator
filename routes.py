import copy
import os
import random
from collections import defaultdict

import requests
from tenacity import retry, stop_after_attempt, wait_fixed
from web3 import Web3

from rebalance_server.apr_utils import convert_apy_to_apr
from rebalance_server.main import load_evm_raw_positions, main

RADIANT_USER_ADDRESS = "0x43cd745Bd5FbFc8CfD79ebC855f949abc79a1E0C"
RADIANT_MULTI_FEE_DISTRIBUTION = "0x76ba3eC5f5adBf1C58c91e86502232317EeA72dE"
W3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URL")))
# v1
# [
#     "0xC6a58A8494E61fc4EF04F6075c4541C9664ADcC9",
#     "0x271E3409093f7ECffFB2a1C82e5E87B2ecB3E310",
#     "0x549caec2C863a04853Fb829aac4190E1B50df0Cc",
#     "0xE66c4EA218Cdb8DCbCf3f605ed1aC29461CBa4b8",
# ]
CONTRACT_ADDRESS = [
    "0xA3CDd5a4b9f5a69C5C3a297A428A10B742F1c6E1",
    "0xBb4D0819089879d83ae13fEe71aBeAa345629389",
    "0x0F658FC0C72A729F1B8F8444601D657D3F30Db41",
    "0x5073bf9aE65963A5881F36560072adf5d4c6e870",
    "0x4999AE9fDD361Ca6278B0295dd65776b4587E1aA",
    "0x99E9cE14C807e95329a2A35aDD52683528e53231",
]


def get_debank_data():
    evm_positions = load_evm_raw_positions(
        "debank",
        CONTRACT_ADDRESS,
        useCache=True if random.random() > 0.2 else False,
    )
    token_metadata_table: dict[str, dict] = {}
    for position in evm_positions["data"]["result"]["data"]:
        for portfolio_item in position["portfolio_item_list"]:
            for token in portfolio_item["detail"].get(
                "reward_token_list", []
            ) + portfolio_item["detail"].get("supply_token_list", []):
                payload = {
                    "img": token["logo_url"],
                    "price": token["price"],
                    "symbol": token["symbol"],
                    "chain": token["chain"],
                }
                token_metadata_table[f'{token["chain"]}:{token["id"]}'] = payload
                if token["symbol"] == "WETH" and token["chain"] != "bsc":
                    ethPayload = copy.copy(payload)
                    ethPayload["symbol"] = "ETH"
                    ethPayload[
                        "img"
                    ] = "https://static.debank.com/image/token/logo_url/eth/935ae4e4d1d12d59a99717a24f2540b5.png"
                    token_metadata_table[
                        f"{token['chain']}:0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
                    ] = ethPayload
                elif token["symbol"] == "WETH" and token["chain"] != "bsc":
                    token_metadata_table = _handle_native_token_for_each_chain(
                        token, payload, token_metadata_table
                    )
    token_metadata_table = _get_price_of_radiant_rToken(token_metadata_table)
    return token_metadata_table


def get_APR_composition(portfolio_name: str):
    portfolio_apr = main(
        defi_portfolio_service_name="debank",
        optimize_apr_mode="new_pool",
        strategy_name="all_weather_portfolio",
        addresses=CONTRACT_ADDRESS,
    )["portfolio_apr"]

    apr_composition = {}
    if portfolio_name == "permanent_portfolio":
        equilibria_market_addrs = {
            "Equilibria-GDAI": {
                "pool_addr": "0xa0192f6567f8f5DC38C53323235FD08b318D2dcA",
                "ratio": 0.12,
            },
            "Equilibria-GLP": {
                "pool_addr": "0x7D49E5Adc0EAAD9C027857767638613253eF125f",
                "ratio": 0.35,
            },
            "Equilibria-RETH": {
                "pool_addr": "0x14FbC760eFaF36781cB0eb3Cb255aD976117B9Bd",
                "ratio": 0.06,
            },
            "Equilibria-PENDLE": {
                "pool_addr": "0x24e4Df37ea00C4954d668e3ce19fFdcffDEc2cF6",
                "ratio": 0.24,
            },
        }
        for key, pool_metadata in equilibria_market_addrs.items():
            apr_composition[key] = _fetch_equilibria_APR_composition(
                pool_metadata["pool_addr"], ratio=pool_metadata["ratio"]
            )
        apr_composition["SushiSwap-MagicETH"] = _fetch_sushiswap_APR_composition(
            "0xb7e50106a5bd3cf21af210a755f9c8740890a8c9", ratio=0.08
        )
        if apr_composition["SushiSwap-MagicETH"] == {}:
            del apr_composition["SushiSwap-MagicETH"]
        apr_composition["RadiantArbitrum-DLP"] = _fetch_radiant_APR_composition(
            ratio=0.15
        )
        return _calculate_aggr_apr_composition(
            apr_composition, portfolio_apr=portfolio_apr
        )
    raise NotImplementedError(f"Portfolio {portfolio_name} is not implemented")


@retry(stop=stop_after_attempt(5), wait=wait_fixed(5))
def fetch_1inch_swap_data(
    chain_id: int,
    from_token_address: str,
    to_token_address: str,
    amount: str,
    from_address: str,
    slippage: int,
):
    url = f"https://api.1inch.dev/swap/v5.2/{chain_id}/swap?src={from_token_address}&dst={to_token_address}&amount={amount}&from={from_address}&slippage={slippage}&disableEstimate=true"
    headers = {
        "Authorization": f"Bearer {os.getenv('ONE_INCH_API_KEY')}",
        "Accept": "application/json",
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Will trigger a retry if HTTP error
    return response.json()


def _fetch_equilibria_APR_composition(pool_addr: str, ratio: float) -> float:
    result = defaultdict(lambda: defaultdict(float))
    equilibria_chain_info_map = requests.get("https://equilibria.fi/api/chain-info-map")
    if equilibria_chain_info_map.status_code != 200:
        raise Exception("Failed to fetch equilibria chain info map")
    equilibria_chain_info_map = equilibria_chain_info_map.json()
    result["Underlying APY"]["token"] = []
    pool_info = [
        pl
        for pl in equilibria_chain_info_map["42161"]["poolInfos"]
        if pl["market"] == pool_addr and pl["shutdown"] is False
    ][0]
    for category, keys in {
        "Swap Fee": ["swapFeeApy"],
        "Underlying APY": ["underlyingApy", "lpRewardApy"],
        "PENDLE": ["pendleApy"],
    }.items():
        for key in keys:
            result[category]["APR"] += (
                convert_apy_to_apr(pool_info["marketInfo"][key]) * ratio
            )
        if category == "PENDLE":
            result["PENDLE"][
                "token"
            ] = "arb:0x0c880f6761F1af8d9Aa9C466984b80DAb9a8c9e8".lower()
            result["PENDLE"]["APR"] = (
                convert_apy_to_apr(
                    pool_info["pendleBoostedApy"]
                    - pool_info["pendleApy"]
                    + pool_info["pendleBaseBoostableApy"]
                )
                * ratio
            )
            result["EQB"][
                "token"
            ] = "arb:0xBfbCFe8873fE28Dfa25f1099282b088D52bbAD9C".lower()
            result["EQB"]["APR"] = convert_apy_to_apr(pool_info["eqbApy"]) * ratio
            # TODO(david): uncomment xEQB once we can redeem xEQB for user
            # result["xEQB"]["token"] = "0x96C4A48Abdf781e9c931cfA92EC0167Ba219ad8E".lower()
            # result["xEQB"]["APR"] = convert_apy_to_apr(pool_info["xEqbApy"])
        elif category == "Underlying APY":
            for reward in pool_info["marketInfo"]["underlyingRewardApyBreakdown"]:
                result[category]["token"].append(
                    f'arb:{reward["asset"]["address"].lower()}'
                )
            result[category]["token"].append(
                f'arb:{pool_info["marketInfo"]["basePricingAsset"]["address"]}'
            )
    return result


def _fetch_sushiswap_APR_composition(pool_addr: str, ratio: float) -> float:
    result = defaultdict(lambda: defaultdict(float))
    pool_res = requests.get(f"https://pools.sushi.com/api/v0/42161/{pool_addr}")
    if pool_res.status_code != 200:
        return {}
        # raise Exception("Failed to fetch kava sushiswap APR")
    pool_json = pool_res.json()
    for incentive in pool_json["incentives"]:
        if incentive["apr"] > 0:
            symbol = incentive["rewardToken"]["symbol"]
            result[symbol][
                "token"
            ] = f'arb:{incentive["rewardToken"]["address"].lower()}'
            result[symbol]["APR"] = incentive["apr"] * ratio

    result["Swap Fee"]["APR"] = pool_json["feeApr1d"] * ratio
    return result


def _fetch_radiant_APR_composition(ratio: float) -> float:
    abi = '[{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"claimableRewards","outputs":[{"components":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"internalType":"struct IFeeDistribution.RewardData[]","name":"rewardsData","type":"tuple[]"}],"stateMutability":"view","type":"function"}]'
    radiant_contract = W3.eth.contract(address=RADIANT_MULTI_FEE_DISTRIBUTION, abi=abi)

    token_metadata = get_debank_data()
    claimableRewards = radiant_contract.functions.claimableRewards(
        RADIANT_USER_ADDRESS
    ).call()
    claimableRewardsDict = {}
    for token_addr, balance in claimableRewards:
        if balance == 0:
            continue
        normalized_token_addr = token_addr.lower()
        token_addr_with_chain_info = f"arb:{normalized_token_addr}"
        if token_addr_with_chain_info not in token_metadata:
            raise Exception(f"token {token_addr_with_chain_info} not found")
        claimableRewardsDict[token_addr_with_chain_info] = (
            balance
            / _get_decimal_per_token(normalized_token_addr)
            * token_metadata[token_addr_with_chain_info]["price"]
        )
    sum_of_claimable_rewards = sum(claimableRewardsDict.values())

    radiant_apr_composition_dict = {}
    for token_addr in claimableRewardsDict:
        usd_denominated_value = claimableRewardsDict[token_addr]
        symbol = token_metadata[token_addr]["symbol"]
        radiant_apr_composition_dict[symbol] = {
            "APR": usd_denominated_value / sum_of_claimable_rewards * ratio,
            "token": token_addr,
        }
    return radiant_apr_composition_dict


def _handle_native_token_for_each_chain(
    token: dict, payload: dict, token_metadata_table: dict
) -> dict:
    ethPayload = copy.copy(payload)
    ethPayload["symbol"] = "ETH"
    ethPayload[
        "img"
    ] = "https://static.debank.com/image/token/logo_url/eth/935ae4e4d1d12d59a99717a24f2540b5.png"
    token_metadata_table[
        f"{token['chain']}:0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
    ] = ethPayload
    return token_metadata_table


def _get_price_of_radiant_rToken(token_metadata_table: dict) -> dict:
    mapping_from_native_token_to_rtoken = {
        "0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9": "0xd69d402d1bdb9a2b8c3d88d98b9ceaf9e4cd72d9",
        "0xff970a61a04b1ca14834a43f5de4533ebddb5cc8": "0x48a29e756cc1c097388f3b2f3b570ed270423b3d",
        "0xda10009cbd5d07dd0cecc66161fc93d7c9000da1": "0x0d914606f3424804fa1bbbe56ccc3416733acec6",
        "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee": "0x0df5dfd95966753f01cb80e76dc20ea958238c46",
        "0x5979d7b546e38e414f7e9822514be443a4800529": "0x42c248d137512907048021b30d9da17f48b5b7b2",
        "0x912ce59144191c1204e64559fe8253a0e49e6548": "0x2dade5b7df9da3a7e1c9748d169cd6dff77e3d01",
        "0x3082cc23568ea640225c2467653db90e9250aaa0": "0x3082cc23568ea640225c2467653db90e9250aaa0",
        "0x2f2a2543b76a4166549f7aab2e75bef0aefc5b0f": "0x727354712bdfcd8596a3852fd2065b3c34f4f770",
        "0x82af49447d8a07e3bd95bd0d56f35241523fbab1": "0x0df5dfd95966753f01cb80e76dc20ea958238c46",
    }
    for native_token_addr in mapping_from_native_token_to_rtoken:
        rtoken_addr = mapping_from_native_token_to_rtoken[native_token_addr]
        if native_token_addr in mapping_from_native_token_to_rtoken:
            token_metadata_table[f"arb:{rtoken_addr}"] = token_metadata_table[
                f"arb:{native_token_addr}"
            ]
        else:
            raise NotImplementedError(f"{native_token_addr} not found")
    return token_metadata_table


def _get_decimal_per_token(token_addr: str) -> int:
    if token_addr in [
        "0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9",
        "0xd69d402d1bdb9a2b8c3d88d98b9ceaf9e4cd72d9",
        "0xff970a61a04b1ca14834a43f5de4533ebddb5cc8",
        "0x48a29e756cc1c097388f3b2f3b570ed270423b3d",
    ]:
        return 1e6
    elif token_addr in [
        "0x2f2a2543b76a4166549f7aab2e75bef0aefc5b0f",
        "0x727354712bdfcd8596a3852fd2065b3c34f4f770",
    ]:
        return 1e8
    return 1e18


def _calculate_aggr_apr_composition(
    apr_composition: dict, portfolio_apr: float
) -> dict:
    aggregated_result = defaultdict(lambda: defaultdict(float))
    for metadata_of_tokens in apr_composition.values():
        for token_symbol, metadata in metadata_of_tokens.items():
            aggregated_result[token_symbol]["APR"] += metadata["APR"]
            aggregated_result[token_symbol]["token"] = metadata["token"]
    apr_composition["aggregated_apr_composition"] = aggregated_result
    ratio_of_apr_from_each_protocol_to_defillama_apr = (
        _normalize_the_ratio_for_APR_from_each_protocol_API_to_defillama_apr(
            apr_composition, portfolio_apr
        )
    )
    for metadata in apr_composition["aggregated_apr_composition"].values():
        metadata["APR"] *= ratio_of_apr_from_each_protocol_to_defillama_apr
    return apr_composition


def _normalize_the_ratio_for_APR_from_each_protocol_API_to_defillama_apr(
    apr_composition: dict, portfolio_apr: float
) -> dict:
    # there's discrepancy between defillama APR and APR from each protocol's API
    # to make it consistent, we need to normalize the APR from each protocol's API to defillama APR
    sum_of_apr_from_each_protocol = sum(
        [
            metadata["APR"]
            for metadata in apr_composition["aggregated_apr_composition"].values()
        ]
    )
    return portfolio_apr / 100 / sum_of_apr_from_each_protocol
