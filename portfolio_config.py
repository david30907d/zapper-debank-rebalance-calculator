MIN_REBALANCE_POSITION_THRESHOLD = 500
DEFILLAMA_API_REQUEST_FREQUENCY_RECIPROCAL = 50
BLACKLIST_CHAINS = {"Avalanche", "BSC", "Solana"}
BLACKLIST_CHAINS_FOR_STABLE_COIN = {"Ethereum"}
BLACKLIST_PROTOCOL = {"rehold", "deri-protocol"}
STABLE_COIN_WHITELIST = {"USDT", "USDC"}
DEBANK_ADDRESS = {
    "0x76ba3ec5f5adbf1c58c91e86502232317eea72de": {
        "categories": ["large_cap_us_stocks", "long_term_bond"],
        "symbol": "RDNT-ETH",
        "defillama-APY-pool-id": "118281c6-3a4a-4324-b804-5664617df77d",
        "tags": ["rdnt", "eth"],
        "composition": {"eth": 0.2, "rdnt": 0.8},
        "project": "radiant",
    },
    "0xb7e50106a5bd3cf21af210a755f9c8740890a8c9": {
        "categories": ["small_cap_us_stocks", "long_term_bond"],
        "symbol": "MAGIC-WETH",
        "defillama-APY-pool-id": "afb71713-9c2e-4717-a8a3-9f959b966e49",
        "tags": ["magic", "eth"],
        "composition": {"eth": 0.5, "magic": 0.5},
        "project": "uniswap-v3",
    },
    "0x5fbbef48ce0850e5a73bc3f4a6e903458b3c0af4": {
        "categories": ["large_cap_us_stocks", "long_term_bond"],
        "project": "trader-joe",
        "symbol": "weth-gmx-TJ-LP-arb",
        "DEFAULT_APR": 0,
        "tags": ["eth", "gmx"],
        "composition": {"eth": 0.5, "gmx": 0.5},
    },
    "0x127963a74c07f72d862f2bdc225226c3251bd117": {
        "categories": ["intermediate_term_bond"],
        "symbol": "VST-FRAX",
        "defillama-APY-pool-id": "ca8b6649-b825-41c7-8955-47b955b37bb0",
        "tags": ["vst", "frax"],
        "composition": {"vst": 0.5, "frax": 0.5},
        "project": "frax",
    },
    "0x673cf5ab7b44caac43c80de5b99a37ed5b3e4cc6": {
        "categories": ["intermediate_term_bond"],
        "symbol": "DAI",
        "defillama-APY-pool-id": "15c3e528-2825-4ca4-804b-406e8b8e2ebd",
        "tags": ["gdai"],
        "composition": {"dai": 1},
        "project": "gains-network",
    },
    "0x4e971a87900b931ff39d1aad67697f49835400b6": {
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
        "project": "gmx",
    },
    "0xbdec4a045446f583dc564c0a227ffd475b329bf0": {
        "categories": ["gold", "long_term_bond", "intermediate_term_bond"],
        "symbol": "WETH-DAI",
        "defillama-APY-pool-id": "592db49f-ac12-4072-b659-4e4a29c2b197",
        "tags": ["dai", "eth"],
        "composition": {"eth": 0.5, "dai": 0.5},
        "project": "kyberswap-elastic",
    },
    "0x3d9819210a31b4961b30ef54be2aed79b9c9cd3b": {
        "categories": ["intermediate_term_bond"],
        "project": "compound",
        "symbol": "compound USDT",
        "DEFAULT_APR": 0.02,
        "tags": ["cusdt"],
        "composition": {"usdt": 1},
    },
    "0x41a5881c17185383e19df6fa4ec158a6f4851a69": {
        "categories": ["intermediate_term_bond"],
        "symbol": "OHMFRAXBP-F",
        "defillama-APY-pool-id": "4f000353-5bb0-4e8c-ad03-194f0662680d",
        "tags": ["ohm", "frax", "usdc"],
        "composition": {"ohm": 0.5, "frax": 0.25, "usdc": 0.25},
        "project": "yearn-finance",
    },
    "0xf562b2f33b3c90d5d273f88cdf0ced866e17092e": {
        "categories": ["intermediate_term_bond"],
        "symbol": "OHM-FRAX",
        "defillama-APY-pool-id": "41e4d018-b7df-422d-93af-d7d4ff94b300",
        "tags": ["frax", "ohm"],
        "composition": {"ohm": 0.5, "frax": 0.5},
        "project": "frax",
    },
    "0x4804357ace69330524ceb18f2a647c3c162e1f95": {
        "categories": ["non_us_developed_market_stocks"],
        "symbol": "WKAVA",
        "defillama-APY-pool-id": "d09a22df-779c-4917-b66f-9e57b2f379f6",
        "tags": ["kava"],
        "composition": {"kava": 1},
        "project": "mare-finance",
    },
    "0xf4b1486dd74d07706052a33d31d7c0aafd0659e1": {
        "categories": ["long_term_bond"],
        "project": "radiant",
        "symbol": "Radiant-ETH-lending",
        "DEFAULT_APR": 0.09,
        "tags": ["eth"],
        "composition": {"eth": 1},
    },
    "0x4fd9f7c5ca0829a656561486bada018505dfcb5e": {
        "categories": ["large_cap_us_stocks", "commodities"],
        "symbol": "RDNT-BNB",
        "defillama-APY-pool-id": "118281c6-3a4a-4324-b804-5664617df77d",
        "tags": ["rdnt", "bnb"],
        "composition": {"bnb": 0.5, "rdnt": 0.5},
        "project": "radiant",
    },
    "0xd50cf00b6e600dd036ba8ef475677d816d6c4281": {
        "categories": ["long_term_bond"],
        "project": "radiant",
        "symbol": "lending",
        "DEFAULT_APR": 0.07,
        "tags": ["eth"],
        "composition": {"eth": 1},
    },
    "0x21178dd2ba9caee9df37f2d5f89a097d69fb0a7d": {
        "categories": ["small_cap_us_stocks", "long_term_bond"],
        "symbol": "MAGIC-WETH",
        "defillama-APY-pool-id": "98d1d43f-dacf-42c3-b2f9-259d34ec930d",
        "tags": ["magic", "eth"],
        "composition": {"eth": 0.5, "magic": 0.5},
        "project": "gamma",
    },
    "0x9dbbbaecacedf53d5caa295b8293c1def2055adc": {
        "categories": [
            "large_cap_us_stocks",
            "long_term_bond",
            "intermediate_term_bond",
            "gold",
        ],
        "symbol": "WETH-WBTC-LINK-UNI-USDC-USDT-DAI-FRAX",
        "defillama-APY-pool-id": "79587734-a461-4f4c-b9e2-c85c70484cf8",
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
        "project": "beefy",
    },
    "0x1f36f95a02c744f2b3cd196b5e44e749c153d3b9": {
        "categories": ["small_cap_us_stocks"],
        "symbol": "VELO-OP",
        "defillama-APY-pool-id": "d268cba2-bf82-43c7-b4dc-1e8f2c37e150",
        "tags": ["velo", "op"],
        "composition": {"velo": 0.5, "op": 0.5},
        "project": "velodrome",
    },
    "0x6b8edc43de878fd5cd5113c42747d32500db3873": {
        "categories": ["small_cap_us_stocks", "intermediate_term_bond", "gold"],
        "symbol": "VELO-USDC",
        "defillama-APY-pool-id": "6e053f06-e90d-4f16-b31b-d615d33f26f5",
        "tags": ["velo", "usdc"],
        "composition": {"velo": 0.5, "usdc": 0.5},
        "project": "pickle",
    },
    "0x9c7305eb78a432ced5c4d14cac27e8ed569a2e26": {
        "categories": ["small_cap_us_stocks"],
        "project": "velodrome",
        "symbol": "velodrome-lock",
        "DEFAULT_APR": 0.0001,
        "tags": ["velo"],
        "composition": {"velo": 1},
    },
    "0x085a2054c51ea5c91dbf7f90d65e728c0f2a270f": {
        "categories": ["long_term_bond", "commodities", "large_cap_us_stocks"],
        "symbol": "WETH-CRV",
        "defillama-APY-pool-id": "caad8223-bae8-4ef4-bdf3-c12cc55c94e3",
        "tags": ["crv", "eth"],
        "composition": {"eth": 0.5, "crv": 0.5},
        "project": "convex-finance",
    },
    "0x20ec0d06f447d550fc6edee42121bc8c1817b97d": {
        "categories": ["long_term_bond", "commodities"],
        "symbol": "WMATIC-WETH",
        "defillama-APY-pool-id": "1f23a6a9-84d0-4cf9-b978-aba431703757",
        "tags": ["matic", "eth"],
        "composition": {"eth": 0.5, "matic": 0.5},
        "project": "gamma",
    },
    # "0x3355df6D4c9C3035724Fd0e3914dE96A5a83aaf4": {
    "0xacf5a67f2fcfeda3946ccb1ad9d16d2eb65c3c96": {
        "categories": ["long_term_bond", "intermediate_term_bond", "gold"],
        "project": "SpaceFi",
        "symbol": "USDC-ETH",
        "DEFAULT_APR": 0.31,
        "tags": ["usdc", "eth"],
        "composition": {"eth": 0.5, "usdc": 0.5},
        "forAirdrop": True,
    },
    "0x7d49e5adc0eaad9c027857767638613253ef125f": {
        "categories": [
            "large_cap_us_stocks",
            "long_term_bond",
            "intermediate_term_bond",
            "gold",
        ],
        "symbol": "GLP",
        "defillama-APY-pool-id": "24524d98-7fa5-47ca-b788-e7879319176c",
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
            # putting pt token as 0% since PT token doesn't change the composition of this LP token
            "pt-glp-28mar2024": 0,
        },
        "project": "pendle",
    },
    "0xa0192f6567f8f5dc38c53323235fd08b318d2dca": {
        "categories": ["intermediate_term_bond"],
        "symbol": "GDAI",
        "defillama-APY-pool-id": "95c950d1-8479-42b3-852c-282ed30c1f6c",
        "tags": ["gdai"],
        "composition": {"dai": 1},
        "project": "pendle",
    },
    "0x2ec8c498ec997ad963969a2c93bf7150a1f5b213": {
        "categories": ["long_term_bond"],
        "symbol": "RETH-WETH",
        # "defillama-APY-pool-id": "2811f0f5-18cf-4b72-a9d4-55c2c7ed577c",
        "DEFAULT_APR": 0.209,
        "tags": ["eth"],
        "composition": {"eth": 1},
        "project": "pendle",
    },
    "0xd85e038593d7a098614721eae955ec2022b9b91b": {
        "categories": ["intermediate_term_bond"],
        "symbol": "DAI",
        "defillama-APY-pool-id": "15c3e528-2825-4ca4-804b-406e8b8e2ebd",
        "tags": ["gdai"],
        "composition": {"dai": 1},
        "project": "gains-network",
    },
    "0xf4d73326c13a4fc5fd7a064217e12780e9bd62c3": {
        "categories": ["small_cap_us_stocks", "long_term_bond"],
        "symbol": "DPX-WETH",
        "defillama-APY-pool-id": "97cb382d-8dc4-4e17-b0f6-b6b51994dbeb",
        "tags": ["dpx", "eth"],
        "composition": {"eth": 0.5, "dpx": 0.5},
        "project": "sushiswap",
    },
    "0x72a19342e8f1838460ebfccef09f6585e32db86e": {
        "categories": ["small_cap_us_stocks", "commodities"],
        "symbol": "CVX",
        "DEFAULT_APR": 0.2,
        "tags": ["cvx"],
        "composition": {"cvx": 1},
        "project": "convex-finance",
    },
    "0xaa0c3f5f7dfd688c6e646f66cd2a6b66acdbe434": {
        "categories": ["large_cap_us_stocks", "commodities"],
        "symbol": "CVXCRV",
        "defillama-APY-pool-id": "ef32dd3b-a03b-4f79-9b65-8420d7e04ad0",
        "tags": ["cvxcrv"],
        "composition": {"cvxcrv": 1},
        "project": "convex-finance",
    },
    "0xc96e1a26264d965078bd01eaceb129a65c09ffe7": {
        "categories": ["intermediate_term_bond"],
        "symbol": "OHMFRAXBP-F",
        "defillama-APY-pool-id": "4f000353-5bb0-4e8c-ad03-194f0662680d",
        "tags": ["ohm", "frax", "usdc"],
        "composition": {"ohm": 0.5, "frax": 0.25, "usdc": 0.25},
        "project": "yearn-finance",
    },
    "0x34101fe647ba02238256b5c5a58aeaa2e532a049": {
        "categories": ["intermediate_term_bond"],
        "symbol": "USDT",
        "defillama-APY-pool-id": "30d03a2d-f857-472d-91e7-d10d6264765c",
        "tags": ["usdt"],
        "composition": {"usdt": 1},
        "project": "gmd-protocol",
    },
    "0x3db4b7da67dd5af61cb9b3c70501b1bdb24b2c22": {
        "categories": ["intermediate_term_bond"],
        "symbol": "USDC",
        "defillama-APY-pool-id": "30d03a2d-f857-472d-91e7-d10d6264765c",
        "tags": ["usdc"],
        "composition": {"usdc": 1},
        "project": "gmd-protocol",
    },
    "0x868a943ca49a63eb0456a00ae098d470915eea0d": {
        "categories": ["intermediate_term_bond"],
        "symbol": "USDC",
        "defillama-APY-pool-id": "1acd3a3f-3ed6-4e24-9333-f1a9e41c3b17",
        "tags": ["usdc"],
        "composition": {"usdc": 1},
        "project": "rehold",
    },
    "0xfff4b05a10c5df1382272e554254ea8b097ec03e": {
        "categories": ["small_cap_us_stocks"],
        "project": "Equilibria",
        "symbol": "PENDLE",
        "DEFAULT_APR": 1.32,
        "tags": ["pendle"],
        "composition": {
            "pendle": 0.5,
        },
    },
    "0x481fcfa00ee6b2384ff0b3c3b5b29ad911c1aaa7": {
        "categories": ["long_term_bond", "commodities"],
        "symbol": "WMATIC-WETH",
        "DEFAULT_APR": 0.23,
        "tags": ["matic", "eth"],
        "composition": {"eth": 0.5, "matic": 0.5},
        "project": "quickswap-dex",
    },
    "0x0fa70bd9b892c7b6d2a9ea8dd1ce446e52f86935": {
        "categories": ["commodities"],
        "project": "stfil",
        "symbol": "FIL",
        "defillama-APY-pool-id": "03cdc005-9fb7-4e0a-9f11-e0155ee4c8bf",
        "tags": ["fil"],
        "composition": {
            "fil": 1,
        },
    },
    "0xc531570e9508fb73a2c223956fa21dbeafb60568": {
        "categories": ["intermediate_term_bond"],
        "project": "auragi-finance",
        "symbol": "USDT-USDC",
        "defillama-APY-pool-id": "a8ffb4ac-47ce-4f23-abee-c88832574c6d",
        "tags": ["usdt", "usdc"],
        "composition": {
            "usdc": 0.5,
            "usdt": 0.5,
        },
        "living-expenses": True,
    },
    "0xeed247ba513a8d6f78be9318399f5ed1a4808f8e": {
        "categories": ["intermediate_term_bond"],
        "project": "tender_lending",
        "symbol": "USDC",
        "defillama-APY-pool-id": "f152ff88-dd31-4efb-a0a9-ad26b5536cc7",
        "tags": ["usdc"],
        "composition": {
            "usdc": 1,
        },
        "living-expenses": True,
    },
}


NANSEN_ADDRESS = {
    "EA1D43981D5C9A1C4AAEA9C23BB1D4FA126BA9BC7020A25E0AE4AA841EA25DC5": {
        "categories": [
            "non_us_emerging_market_stocks",
            "long_term_bond",
        ],
        "project": "Osmosis",
        "symbol": "OSMO-WETH",
        "defillama-APY-pool-id": "5fe464d2-3575-4b70-bc69-cc52d2857e4a",
        "tags": ["osmo", "eth"],
        "composition": {
            "eth": 0.5,
            "osmo": 0.5,
        },
    },
    "57AA1A70A4BC9769C525EBF6386F7A21536E04A79D62E1981EFCEF9428EBB205": {
        "categories": [
            "non_us_emerging_market_stocks",
            "non_us_developed_market_stocks",
        ],
        "project": "Osmosis",
        "symbol": "OSMO-KAVA",
        "defillama-APY-pool-id": "f6efb5eb-b6fc-4ada-8fe2-05702f38d606",
        "tags": ["osmo", "kava"],
        "composition": {
            "kava": 0.5,
            "osmo": 0.5,
        },
    },
    "27394FB092D2ECCD56123C74F36E4C1F926001CEADA9CA97EA622B25F41E5EB2": {
        "categories": ["non_us_emerging_market_stocks"],
        "project": "Osmosis",
        "symbol": "OSMO-ATOM",
        "defillama-APY-pool-id": "4ced8c2d-67c4-4555-b025-be49c110ca58",
        "tags": ["osmo", "atom"],
        "composition": {
            "atom": 0.5,
            "osmo": 0.5,
        },
    },
    "DEC41A02E47658D40FC71E5A35A9C807111F5A6662A3FB5DA84C4E6F53E616B3": {
        "categories": ["non_us_emerging_market_stocks", "commodities"],
        "project": "Cosmos",
        "symbol": "ATOM",
        "DEFAULT_APR": 0.2,
        "tags": ["atom"],
        "composition": {
            "atom": 1,
        },
    },
    "0x371d33963fb89ec9542a11ccf955b3a90391f99f": {
        "categories": ["non_us_developed_market_stocks", "long_term_bond"],
        "project": "Equilibre",
        "symbol": "KAVA-WETH",
        "DEFAULT_APR": 1.1,
        "tags": ["kava", "eth"],
        "composition": {
            "kava": 0.5,
            "eth": 0.5,
        },
    },
    "0xf731202a3cf7efa9368c2d7bd613926f7a144db5": {
        "categories": ["non_us_developed_market_stocks", "long_term_bond"],
        "project": "sushiswap",
        "symbol": "KAVA-WETH",
        "DEFAULT_APR": 0.38,
        "tags": ["kava", "eth"],
        "composition": {
            "kava": 0.5,
            "eth": 0.5,
        },
    },
}

ADDRESS_2_CATEGORY = {
    **DEBANK_ADDRESS,
    **NANSEN_ADDRESS,
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
}

LIQUIDITY_BOOK_PROTOCOL_APR_DISCOUNT_FACTOR = {
    "uniswap-v3": 0.5,
    "kyberswap-elastic": 0.5,
}
