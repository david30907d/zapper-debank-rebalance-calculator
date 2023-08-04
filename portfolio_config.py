import requests

from rebalance_server.apr_utils import convert_apy_to_apr


def fetch_equilibria_APR(chain_id: str, category: str, pool_token: str = "") -> float:
    equilibria_chain_info_map = requests.get("https://equilibria.fi/api/chain-info-map")
    if equilibria_chain_info_map.status_code != 200:
        raise Exception("Failed to fetch equilibria chain info map")
    equilibria_chain_info_map = equilibria_chain_info_map.json()
    if category == "poolInfos":
        for pool in equilibria_chain_info_map[chain_id]["poolInfos"]:
            if pool["token"] == pool_token:
                return convert_apy_to_apr(pool["apy"])
    elif category == "ePendle":
        return convert_apy_to_apr(
            equilibria_chain_info_map[chain_id]["ePendle"]["apy"]
            + equilibria_chain_info_map[chain_id]["ePendle"]["pendleApy"]
        )
    raise Exception(f"Failed to find pool {pool_token} in equilibria chain info map")


def fetch_convex_locked_CVX_APR() -> float:
    api_cvx_locked = requests.get(
        "https://www.convexfinance.com/api/cvx/vlcvx-extra-incentives"
    )
    if api_cvx_locked.status_code != 200:
        raise Exception("Failed to fetch convex locked cvx")
    api_cvx_locked = api_cvx_locked.json()
    return api_cvx_locked["cvxApr"] / 100


def fetch_quickswap_APR(pool_addr: str) -> float:
    pool_res = requests.get(
        "https://wire2.gamma.xyz/quickswap/polygon/hypervisors/allData"
    )
    farm_res = requests.get("https://wire2.gamma.xyz/quickswap/polygon/allRewards2")
    if pool_res.status_code != 200 or farm_res.status_code != 200:
        raise Exception("Failed to fetch quickswap APR")
    pool_json = pool_res.json()
    farm_json = farm_res.json()
    for farm in farm_json.values():
        for farm_pool_addr, farm_pool in farm["pools"].items():
            if farm_pool_addr == pool_addr:
                return (
                    pool_json[pool_addr]["returns"]["daily"]["feeApr"]
                    + farm_pool["apr"]
                )
    raise Exception(f"Failed to find pool {pool_addr} in quickswap")


def fetch_traderjoe_auto_pool_APR(pool_addr: str) -> float:
    pool_res = requests.get("https://barn.traderjoexyz.com/v1/vaults/arbitrum")
    if pool_res.status_code != 200:
        raise Exception("Failed to fetch traderjoe auto pool APR")
    pool_json = pool_res.json()
    for pool in pool_json:
        if pool["address"] == pool_addr:
            return pool["apr1d"]
    raise Exception(f"Failed to find pool {pool_addr} in traderjoe auto pool")


def fetch_kava_sushiswap_APR(pool_addr: str) -> float:
    pool_res = requests.get(f"https://pools.sushi.com/api/v0/2222/{pool_addr}")
    if pool_res.status_code != 200:
        raise Exception("Failed to fetch kava sushiswap APR")
    accumulatedAPR = 0
    pool_json = pool_res.json()
    for incentive in pool_json["incentives"]:
        accumulatedAPR += incentive["apr"]
    accumulatedAPR += pool_json["feeApr1d"]
    return accumulatedAPR


def fetch_kava_lend_APY(pool_addr: str, token: str) -> float:
    pool_res = requests.get("https://api.data.kava.io/kava/incentive/v1beta1/params")
    supplied_coins = requests.get(
        "https://api.data.kava.io/kava/hard/v1beta1/total-deposited"
    )
    price = requests.get("https://api.data.kava.io/kava/pricefeed/v1beta1/prices")
    if (
        pool_res.status_code != 200
        or supplied_coins.status_code != 200
        or price.status_code != 200
    ):
        raise Exception("Failed to fetch kava sushiswap APR")
    pool_json = pool_res.json()
    supplied_coins_json = supplied_coins.json()
    price_json = price.json()
    for pool in pool_json["params"]["hard_supply_reward_periods"]:
        if pool["collateral_type"] == pool_addr:
            targeted_pool_amount = list(
                filter(
                    lambda coin: coin["denom"] == pool_addr,
                    supplied_coins_json["supplied_coins"],
                )
            )
            assert len(targeted_pool_amount) == 1
            targeted_price = list(
                filter(lambda coin: coin["market_id"] == token, price_json["prices"])
            )
            assert len(targeted_price) == 1
            return convert_apy_to_apr(
                float(pool["rewards_per_second"][0]["amount"])
                * 86400
                * 365
                / float(targeted_pool_amount[0]["amount"])
                / float(targeted_price[0]["price"])
            )
    raise Exception(f"Failed to find pool {pool_addr} in kava lend")


def fetch_equilibre_APR(symbol: str) -> float:
    api_pairs = requests.get("https://api.equilibrefinance.com/api/v1/pairs")
    if api_pairs.status_code != 200:
        raise Exception("Failed to fetch equilibre chain info map")
    api_pairs = api_pairs.json()
    for pool in api_pairs["data"]:
        if pool["symbol"] == symbol:
            return pool["apr"] / 100
    raise Exception(f"Failed to find symbol {symbol} in equilibre")


def get_metadata_by_project_symbol(project_symbol: str) -> dict:
    for address_and_project, metadata in ADDRESS_2_CATEGORY.items():
        project = address_and_project.split(":")[-1]
        if f'{project}:{metadata["symbol"]}'.lower() == project_symbol.lower():
            return metadata
    raise Exception(f"Cannot find {project_symbol} in your address mapping table")


MIN_REBALANCE_POSITION_THRESHOLD = 250
DEFILLAMA_API_REQUEST_FREQUENCY_RECIPROCAL = 50
BLACKLIST_CHAINS = {"Avalanche", "BSC", "Solana"}
BLACKLIST_CHAINS_FOR_STABLE_COIN = {"Ethereum"}
BLACKLIST_PROTOCOL = {
    "rehold",
    "deri-protocol",
    "acryptos",
    "filet-finance",
    "yama-finance",
}
STABLE_COIN_WHITELIST = {"USDT", "USDC", "USDT.E", "USDC.E"}
DEBANK_ADDRESS = {
    "0x76ba3ec5f5adbf1c58c91e86502232317eea72de:arb_radiantcapital2": {
        "categories": ["large_cap_us_stocks", "long_term_bond"],
        "symbol": "RDNT-ETH",
        "defillama-APY-pool-id": "118281c6-3a4a-4324-b804-5664617df77d",
        "tags": ["rdnt", "eth"],
        "composition": {"eth": 0.2, "rdnt": 0.8},
    },
    "0xf4d73326c13a4fc5fd7a064217e12780e9bd62c3:13:arb_sushiswap": {
        "categories": ["small_cap_us_stocks", "long_term_bond"],
        "symbol": "MAGIC-WETH",
        "defillama-APY-pool-id": "5f98842f-72cb-4579-807f-403ca2dfb993",
        "tags": ["magic", "eth"],
        "composition": {"eth": 0.5, "magic": 0.5},
    },
    "0x127963a74c07f72d862f2bdc225226c3251bd117:arb_frax": {
        "categories": ["intermediate_term_bond"],
        "symbol": "VST-FRAX",
        "defillama-APY-pool-id": "ca8b6649-b825-41c7-8955-47b955b37bb0",
        "tags": ["vst", "frax"],
        "composition": {"vst": 0.5, "frax": 0.5},
    },
    "0x4e971a87900b931ff39d1aad67697f49835400b6:arb_gmx": {
        "categories": [
            "large_cap_us_stocks",
            "long_term_bond",
            "intermediate_term_bond",
            "gold",
        ],
        "symbol": "GLP",
        "defillama-APY-pool-id": "825688c0-c694-4a6b-8497-177e425b7348",
        "tags": ["glp"],
        "composition": {
            "eth": 0.3,
            "wbtc": 0.25,
            "link": 0.01,
            "uni": 0.01,
            "usdc": 0.34,
            "usdt": 0.02,
            "dai": 0.05,
            "frax": 0.02,
            "mim": 0,
        },
    },
    "0x41a5881c17185383e19df6fa4ec158a6f4851a69:43:convex": {
        "categories": ["intermediate_term_bond"],
        "symbol": "OHMFRAXBP-F",
        "defillama-APY-pool-id": "4f000353-5bb0-4e8c-ad03-194f0662680d",
        "tags": ["ohm", "frax", "usdc"],
        "composition": {"ohm": 0.5, "frax": 0.25, "usdc": 0.25},
    },
    "0xf562b2f33b3c90d5d273f88cdf0ced866e17092e:frax": {
        "categories": ["intermediate_term_bond"],
        "symbol": "OHM-FRAX",
        "defillama-APY-pool-id": "41e4d018-b7df-422d-93af-d7d4ff94b300",
        "tags": ["frax", "ohm"],
        "composition": {"ohm": 0.5, "frax": 0.5},
    },
    "0x4804357ace69330524ceb18f2a647c3c162e1f95:kava_mare": {
        "categories": ["non_us_developed_market_stocks"],
        "symbol": "WKAVA",
        "defillama-APY-pool-id": "d09a22df-779c-4917-b66f-9e57b2f379f6",
        "tags": ["kava"],
        "composition": {"kava": 1},
    },
    "0xf4b1486dd74d07706052a33d31d7c0aafd0659e1:arb_radiantcapital2": {
        "categories": ["long_term_bond"],
        "symbol": "Radiant-ETH-lending",
        "DEFAULT_APR": 0.09,
        "tags": ["eth"],
        "composition": {"eth": 1},
    },
    "0x4fd9f7c5ca0829a656561486bada018505dfcb5e:bsc_radiantcapital2": {
        "categories": ["large_cap_us_stocks", "commodities"],
        "symbol": "RDNT-BNB",
        "defillama-APY-pool-id": "118281c6-3a4a-4324-b804-5664617df77d",
        "tags": ["rdnt", "bnb"],
        "composition": {"bnb": 0.5, "rdnt": 0.5},
    },
    "0xd50cf00b6e600dd036ba8ef475677d816d6c4281:bsc_radiantcapital2": {
        "categories": ["long_term_bond"],
        "symbol": "lending",
        "DEFAULT_APR": 0.07,
        "tags": ["eth"],
        "composition": {"eth": 1},
    },
    "0x085a2054c51ea5c91dbf7f90d65e728c0f2a270f:convex": {
        "categories": ["long_term_bond", "commodities", "large_cap_us_stocks"],
        "symbol": "WETH-CRV",
        "defillama-APY-pool-id": "caad8223-bae8-4ef4-bdf3-c12cc55c94e3",
        "tags": ["crv", "eth"],
        "composition": {"eth": 0.5, "crv": 0.5},
        "project": "convex-finance",
    },
    "0xacf5a67f2fcfeda3946ccb1ad9d16d2eb65c3c96:10:era_spacefi": {
        "categories": ["long_term_bond", "intermediate_term_bond", "gold"],
        "symbol": "USDT-ETH",
        "DEFAULT_APR": 0.23,
        "tags": ["usdt", "eth"],
        "composition": {"eth": 0.5, "usdt": 0.5},
    },
    "0xacf5a67f2fcfeda3946ccb1ad9d16d2eb65c3c96:1:era_spacefi": {
        "categories": ["long_term_bond", "intermediate_term_bond", "gold"],
        "symbol": "USDT-ETH",
        "DEFAULT_APR": 0.23,
        "tags": ["usdt", "eth"],
        "composition": {"eth": 0.5, "usdt": 0.5},
    },
    "0xacf5a67f2fcfeda3946ccb1ad9d16d2eb65c3c96:0:era_spacefi": {
        "categories": ["long_term_bond", "intermediate_term_bond", "gold"],
        "symbol": "SPACE",
        "DEFAULT_APR": 1,
        "tags": ["space"],
        "composition": {"space": 1},
    },
    "0xa0192f6567f8f5dc38c53323235fd08b318d2dca:arb_pendle2": {
        "categories": ["intermediate_term_bond"],
        "symbol": "GDAI",
        "defillama-APY-pool-id": "95c950d1-8479-42b3-852c-282ed30c1f6c",
        "tags": ["gdai"],
        "composition": {"dai": 1},
        "project": "pendle",
    },
    "0xf4d73326c13a4fc5fd7a064217e12780e9bd62c3:17:arb_sushiswap": {
        "categories": ["small_cap_us_stocks", "long_term_bond"],
        "symbol": "DPX-WETH",
        "defillama-APY-pool-id": "97cb382d-8dc4-4e17-b0f6-b6b51994dbeb",
        "tags": ["dpx", "eth"],
        "composition": {"eth": 0.5, "dpx": 0.5},
    },
    "0x72a19342e8f1838460ebfccef09f6585e32db86e:convex": {
        "categories": ["small_cap_us_stocks", "commodities"],
        "symbol": "CVX",
        "APR": fetch_convex_locked_CVX_APR(),
        "tags": ["cvx"],
        "composition": {"cvx": 1},
        "project": "convex-finance",
    },
    "0xc96e1a26264d965078bd01eaceb129a65c09ffe7:frax": {
        "categories": ["intermediate_term_bond"],
        "symbol": "OHMFRAXBP-F",
        "defillama-APY-pool-id": "4f000353-5bb0-4e8c-ad03-194f0662680d",
        "tags": ["ohm", "frax", "usdc"],
        "composition": {"ohm": 0.5, "frax": 0.25, "usdc": 0.25},
        "project": "yearn-finance",
    },
    "0x3db4b7da67dd5af61cb9b3c70501b1bdb24b2c22:arb_gmd": {
        "categories": ["intermediate_term_bond"],
        "symbol": "USDC",
        "defillama-APY-pool-id": "30d03a2d-f857-472d-91e7-d10d6264765c",
        "tags": ["usdc"],
        "composition": {"usdc": 1},
        "project": "gmd-protocol",
    },
    "0x0fa70bd9b892c7b6d2a9ea8dd1ce446e52f86935:fvm_hashking": {
        "categories": ["non_us_emerging_market_stocks"],
        "project": "hashking",
        "symbol": "FIL",
        "defillama-APY-pool-id": "58c3d410-1d51-4c59-bb89-494e042f79ca",
        "tags": ["fil"],
        "composition": {
            "fil": 1,
        },
    },
    "0x4d32c8ff2facc771ec7efc70d6a8468bc30c26bf:1:arb_equilibria": {
        "categories": [
            "large_cap_us_stocks",
            "long_term_bond",
            "intermediate_term_bond",
            "gold",
        ],
        "symbol": "GLP",
        "APR": fetch_equilibria_APR(
            chain_id="42161",
            category="poolInfos",
            pool_token="0xb0D7182Ba15eD02326590f033F72c393C978EB7a",
        ),
        "tags": ["glp"],
        "composition": {
            "eth": 0.3,
            "wbtc": 0.25,
            "link": 0.01,
            "uni": 0.01,
            "usdc": 0.34,
            "usdt": 0.02,
            "dai": 0.05,
            "frax": 0.02,
            "mim": 0,
        },
        "project": "arb_equilibria",
    },
    "0x4d32c8ff2facc771ec7efc70d6a8468bc30c26bf:1:bsc_equilibria": {
        "categories": [
            "long_term_bond",
        ],
        "symbol": "frxETH",
        "APR": fetch_equilibria_APR(
            chain_id="56",
            category="poolInfos",
            pool_token="0x55F140ABbf87EF957263F04Ed75d1691980433A8",
        ),
        "tags": ["eth"],
        "composition": {
            "eth": 1,
        },
        "project": "bsc_equilibria",
    },
    "0x4d32c8ff2facc771ec7efc70d6a8468bc30c26bf:4:arb_equilibria": {
        "categories": [
            "long_term_bond",
            "small_cap_us_stocks",
        ],
        "symbol": "PENDLE-WETH",
        "APR": fetch_equilibria_APR(
            chain_id="42161",
            category="poolInfos",
            pool_token="0x7a2d44931fA2953f812676e05039F488144763F4",
        ),
        "tags": ["eth", "pendle"],
        "composition": {
            "eth": 0.5,
            "pendle": 0.5,
        },
        "project": "arb_equilibria",
    },
    "0x71e0ce200a10f0bbfb9f924fe466acf0b7401ebf:arb_equilibria": {
        "categories": ["small_cap_us_stocks"],
        "symbol": "PENDLE-stake2",
        "APR": fetch_equilibria_APR(chain_id="42161", category="ePendle"),
        "tags": ["pendle"],
        "composition": {
            "pendle": 1,
        },
    },
    "0xb19e477b959751afd4a1c6880525e0390560681e:kava_equilibre": {
        "categories": [
            "non_us_developed_market_stocks",
            "long_term_bond",
        ],
        "project": "kava_equilibre",
        "symbol": "ETH-WKAVA",
        "defillama-APY-pool-id": "e8a518dd-ccfc-43d9-b7e9-8ef3c0d4a68e",
        "tags": ["kava", "eth"],
        "composition": {
            "kava": 0.5,
            "eth": 0.5,
        },
    },
    "0x5383deb37479599a33584f7bbc346ab299e30ff0:kava_equilibre": {
        "categories": [
            "non_us_developed_market_stocks",
            "intermediate_term_bond",
        ],
        "project": "kava_equilibre",
        "symbol": "KAVA-USDT",
        "defillama-APY-pool-id": "3e5781f8-5240-4a55-955b-67abea1bcfeb",
        "tags": ["kava", "usdt"],
        "composition": {
            "kava": 0.5,
            "usdt": 0.5,
        },
    },
    "0xf731202a3cf7efa9368c2d7bd613926f7a144db5:9:kava_sushiswap": {
        "categories": [
            "non_us_developed_market_stocks",
            "intermediate_term_bond",
        ],
        "project": "sushiswap",
        "symbol": "USDC-WKAVA",
        "APR": fetch_kava_sushiswap_APR(
            pool_addr="0xb379eb428a28a927a16ee7f95100ac6a5117aaa1"
        ),
        "tags": ["kava", "usdc"],
        "composition": {
            "kava": 0.5,
            "usdc": 0.5,
        },
    },
    "0x99b966b099ed886a3dc465b56b874ea12813c498:kava_beefy": {
        "categories": [
            "non_us_developed_market_stocks",
            "intermediate_term_bond",
        ],
        "project": "kava_beefy",
        "symbol": "KAVA-USDT",
        "DEFAULT_APR": 0.6,
        "tags": ["kava", "usdt"],
        "composition": {
            "kava": 0.5,
            "usdt": 0.5,
        },
    },
    "0x8329c9c93b63db8a56a3b9a0c44c2edabd6572a8:op_velodrome2": {
        "categories": ["long_term_bond", "small_cap_us_stocks"],
        "project": "op_velodrome2",
        "symbol": "ETH-VELO",
        "defillama-APY-pool-id": "09921e93-8c35-46fb-94ba-9fe0580a2a88",
        "tags": ["eth", "velo"],
        "composition": {
            "eth": 0.5,
            "velo": 0.5,
        },
    },
    "0xca0d15b4bb6ad730fe40592f9e25a2e052842c92:kava_equilibre": {
        "categories": [
            "non_us_developed_market_stocks",
        ],
        "project": "kava_equilibre",
        "symbol": "KAVA-VARA",
        "APR": fetch_equilibre_APR("vAMM-WKAVA/VARA"),
        "tags": ["kava", "vara"],
        "composition": {
            "kava": 0.5,
            "vara": 0.5,
        },
    },
    "0x46ec4bb184528c3aee6f1419e11b28a97f33d483:linea_syncswap": {
        "categories": ["long_term_bond", "commodities"],
        "project": "linea_syncswap",
        "symbol": "ETH-MATIC",
        "DEFAULT_APR": 0.4,
        "tags": ["eth", "matic"],
        "composition": {
            "eth": 0.5,
            "matic": 0.5,
        },
    },
    "0x0f30716960f0618983ac42be2982ffec181af265:op_velodrome2": {
        "categories": ["commodities", "small_cap_us_stocks"],
        "project": "linea_syncswap",
        "symbol": "OP-VELO",
        "defillama-APY-pool-id": "366c295f-4366-475b-bea3-287292cb5b7a",
        "tags": ["op", "velo"],
        "composition": {
            "op": 0.5,
            "velo": 0.5,
        },
    },
}


ADDRESS_2_CATEGORY = {
    **DEBANK_ADDRESS,
}

# TODO(david): use this one to implement advanced search algorithm. Search for new compositions.
TOKEN_2_CATEGORIES = {
    "long_term_bond": ["eth"],
    "intermediate_term_bond": ["ohm", "gohm", "usdc", "frax", "dai", "gdai"],
    "commodities": ["fil", "cvxcrv", "crv", "cvx", "matic", "bnb"],
    "gold": [],
    "large_cap_us_stocks": [],
    "small_cap_us_stocks": [],
    "non_us_developed_market_stocks": [],
    "non_us_emerging_market_stocks": [],
}

ZAPPER_SYMBOL_2_COINGECKO_MAPPING = {
    "EURS": "stasis-eurs",
    "OHM": "olympus",
    "gOHM": "governance-ohm",
    "BNB": "binancecoin",
    "FRAX": "frax",
    "USDC": "usd-coin",
    "USDC.e": "usd-coin",
    "WBTC": "bitcoin",
    "WBTC.e": "bitcoin",
    "BTC.b": "bitcoin",
    "ETH": "ethereum",
    "WETH": "ethereum",
    "WETH.e": "ethereum",
    "WAVAX": "avalanche-2",
    "WAVAX": "avalanche-2",
    "LINK": "chainlink",
    "UNI": "uniswap",
    "USDT": "tether",
    "DAI": "dai",
    "VST": "vesta-stable",
    "MAGIC": "magic",
    "RDNT": "radiant-capital",
    "DPX": "dopex",
    "CVX": "convex-finance",
    "cvxCRV": "convex-crv",
    "MIM": "magic-internet-money",
    "WKAVA": "kava",
    "KAVA": "kava",
    "FIL": "filecoin",
    "OSMO": "osmosis",
    "ATOM": "cosmos",
    "AVAX": "avalanche",
    "VELO": "velodrome-finance",
    "OP": "optimism",
    "CRV": "curve-dao-token",
    "MATIC": "matic-network",
    # there's no easy way to get the price of the GLP
    # so use jones-glp instead
    "PT-GLP-28MAR2024": "jones-glp",
    "PT-gDAI-28MAR2024": "dai",
    "frxETH": "frax-ether",
    "PT-sfrxETH-26DEC2024": "frax-ether",
    "PT-rETH-WETH_BalancerLP Aura-26DEC2024": "rocket-pool-eth",
    "BTCB": "bitcoin",
    "BUSD": "binance-usd",
    "PENDLE": "pendle",
    "wstETH": "wrapped-steth",
    "ARB": "arbitrum",
    "PT-PENDLE-ETH_Camelot-27JUN2024": None,
    "PT-Thena frxETH-ETH-27JUN2024": "ethereum",
    "USDt": "tether",
    "ePendle": None,
    "VARA": "equilibre",
}

LIQUIDITY_BOOK_PROTOCOL_APR_DISCOUNT_FACTOR = {
    "uniswap-v3": 0.5,
    "kyberswap-elastic": 0.5,
}
