# MIN_REBALANCE_POSITION_THRESHOLD = 500
# lower the bar for eth-dai kyberswap
# TODO(david): higer the bar once that size getting bigger
MIN_REBALANCE_POSITION_THRESHOLD = 378
DEFILLAMA_API_REQUEST_FREQUENCY_RECIPROCAL = 50
ZAPPER_ADDRESS = {
    "0x8ec22ec81e740e0f9310e7318d03c494e62a70cd": {
        "categories": ["intermediate_term_bond"],
        "symbol": "crvEURSUSD",
        "defillama-APY-pool-id": "9cf3f9d1-bc48-4436-8ef9-5ecf786c7a9b",
        "tags": ["eurs", "usdt", "usdc"],
    },
    "0xd2d1162512f927a7e282ef43a362659e4f2a728f": {
        "categories": [
            "large_cap_us_stocks",
            "long_term_bond",
            "intermediate_term_bond",
            "gold",
        ],
        "symbol": "glp-avax",
        "defillama-APY-pool-id": "6a3ddb91-0638-4454-97c1-86dc6d59f32c",
        "tags": ["glp"],
        "composition": {
            "avax": 0.05,
            "weth.e": 0.24,
            "btc.b": 0.2,
            "wbtc.e": 0.03,
            "usdc": 0.45,
            "usdc.e": 0.03,
        },
    },
    "0xa14dbce13c22c97fd99daa0de3b1b480c7c3fdf6": {
        "categories": ["small_cap_us_stocks", "long_term_bond"],
        "symbol": "trader-joe-dpx-weth",
        "DEFAULT_APR": 0,
        "tags": ["dpx", "eth"],
        "composition": {"eth": 0.5, "dpx": 0.5},
    },
    "0xcb0e5bfa72bbb4d16ab5aa0c60601c438f04b4ad": {
        "categories": ["gold", "long_term_bond", "intermediate_term_bond"],
        "symbol": "usdt-weth-sushi-LP",
        "defillama-APY-pool-id": "abe3c385-bde7-4350-9f35-2f574ad592d6",
        "tags": ["usdt", "eth"],
        "composition": {"eth": 0.5, "usdt": 0.5},
    },
    "0x4277f8f2c384827b5273592ff7cebd9f2c1ac258": {
        "categories": [
            "large_cap_us_stocks",
            "long_term_bond",
            "intermediate_term_bond",
            "gold",
        ],
        "symbol": "glp-arbitrum",
        "defillama-APY-pool-id": "825688c0-c694-4a6b-8497-177e425b7348",
        "tags": ["glp"],
        "composition": {
            "eth": 0.28,
            "wbtc": 0.2,
            "link": 0.01,
            "uni": 0.01,
            "usdc": 0.41,
            "usdt": 0.02,
            "dai": 0.05,
            "frax": 0.02,
        },
    },
    "0x100ec08129e0fd59959df93a8b914944a3bbd5df": {
        "categories": ["intermediate_term_bond", "long_term_bond"],
        "symbol": "gohm",
        "DEFAULT_APR": 0.07,
        "tags": ["gohm"],
        "composition": {
            # it's a back of the envolope calculation
            "eth": 0.15,
            "frax": 0.85,
        },
    },
    "0x59bf0545fca0e5ad48e13da269facd2e8c886ba4": {
        "categories": ["intermediate_term_bond"],
        "symbol": "VSTFRAX-f",
        "defillama-APY-pool-id": "ca8b6649-b825-41c7-8955-47b955b37bb0",
        "tags": ["vst", "frax"],
        "composition": {"vst": 0.5, "frax": 0.5},
    },
    "0x81b0dcda53482a2ea9eb496342dc787643323e95": {
        "categories": ["intermediate_term_bond"],
        "symbol": "cvxOHMFRAXBP-f",
        "defillama-APY-pool-id": "4f000353-5bb0-4e8c-ad03-194f0662680d",
        "tags": ["ohm", "frax", "usdc"],
        "composition": {"ohm": 0.5, "frax": 0.25, "usdc": 0.25},
    },
    "0xc96e1a26264d965078bd01eaceb129a65c09ffe7": {
        "categories": ["intermediate_term_bond"],
        "symbol": "stkcvxOHMFRAXBP-f-frax",
        "defillama-APY-pool-id": "4f000353-5bb0-4e8c-ad03-194f0662680d",
        "tags": ["ohm", "frax", "usdc"],
        "composition": {"ohm": 0.5, "frax": 0.25, "usdc": 0.25},
    },
    "0x72a19342e8f1838460ebfccef09f6585e32db86e": {
        "categories": ["small_cap_us_stocks", "commodities"],
        "symbol": "CVX",
        "defillama-APY-pool-id": "777032e6-e815-4f44-90b4-abb98f0f9632",
        "tags": [
            "cvx",
        ],
        "composition": {"cvx": 1},
    },
    "0xaa0c3f5f7dfd688c6e646f66cd2a6b66acdbe434": {
        "categories": ["large_cap_us_stocks", "commodities"],
        "symbol": "cvxCRV",
        "defillama-APY-pool-id": "ef32dd3b-a03b-4f79-9b65-8420d7e04ad0",
        "tags": ["cvxcrv"],
        "composition": {"cvxcrv": 1},
    },
    "0x5769071665eb8db80e7e9226f92336bb2897dcfa": {
        "categories": ["intermediate_term_bond"],
        "symbol": "FraxSwapOHM",
        "defillama-APY-pool-id": "41e4d018-b7df-422d-93af-d7d4ff94b300",
        "tags": ["frax", "ohm"],
        "composition": {
            "ohm": 0.5,
            "frax": 0.5,
        },
    },
    "0xf650c3d88d12db855b8bf7d11be6c55a4e07dcc9": {
        "categories": ["intermediate_term_bond"],
        "symbol": "compound USDT",
        "DEFAULT_APR": 0.02,
        "tags": ["cusdt"],
        "composition": {
            "usdt": 1,
        },
    },
    "0x8d9ba570d6cb60c7e3e0f31343efe75ab8e65fb1": {
        "categories": ["intermediate_term_bond", "long_term_bond"],
        "symbol": "gohm-arb",
        "DEFAULT_APR": 0.07,
        "tags": ["gohm"],
        "composition": {
            # it's a back of the envolope calculation
            "eth": 0.15,
            "frax": 0.85,
        },
    },
    "0x0ab87046fbb341d058f17cbc4c1133f25a20a52f": {
        "categories": ["intermediate_term_bond", "long_term_bond"],
        "symbol": "gohm",
        "DEFAULT_APR": 0.07,
        "tags": ["gohm"],
        "composition": {
            # it's a back of the envolope calculation
            "eth": 0.15,
            "frax": 0.85,
        },
    },
    "0x1f80c96ca521d7247a818a09b0b15c38e3e58a28": {
        "categories": ["small_cap_us_stocks", "long_term_bond"],
        "symbol": "dopex-dpx-weth-LP",
        "defillama-APY-pool-id": "97cb382d-8dc4-4e17-b0f6-b6b51994dbeb",
        "tags": ["dpx", "eth"],
        "composition": {"eth": 0.5, "dpx": 0.5},
    },
    "0xb5c88537d8f5f356e43ec94e20f7eb26bd1ac967": {
        "categories": ["small_cap_us_stocks", "long_term_bond"],
        "symbol": "sushi-DPX-WETH",
        "defillama-APY-pool-id": "97cb382d-8dc4-4e17-b0f6-b6b51994dbeb",
        "tags": ["dpx", "eth"],
        "composition": {"eth": 0.5, "dpx": 0.5},
    },
    "0xb52781c275431bd48d290a4318e338fe0df89eb9": {
        "categories": ["small_cap_us_stocks", "long_term_bond"],
        "symbol": "uniswap-DPX-WETH",
        "defillama-APY-pool-id": "ce53d880-7ebf-40c5-9d97-e4c0fa0bc127",
        "tags": ["dpx", "eth"],
        "composition": {"eth": 0.5, "dpx": 0.5},
    },
    "0xd85e038593d7a098614721eae955ec2022b9b91b": {
        "categories": ["intermediate_term_bond", "long_term_bond"],
        "symbol": "gDAI",
        "defillama-APY-pool-id": "15c3e528-2825-4ca4-804b-406e8b8e2ebd",
        "tags": ["gdai"],
        "composition": {
            # just a back of the envolope calculation
            "eth": 0.36,
            "usdc": 0.64,
        },
    },
    "0x80789d252a288e93b01d82373d767d71a75d9f16": {
        "categories": ["small_cap_us_stocks"],
        "symbol": "veDPX",
        "DEFAULT_APR": 0.13,
        "tags": ["vedpx"],
        "composition": {
            "dpx": 1,
        },
    },
    "0xc8418af6358ffdda74e09ca9cc3fe03ca6adc5b0": {
        "categories": ["small_cap_us_stocks"],
        "symbol": "veFXS",
        "DEFAULT_APR": 0.01,
        "tags": ["vefxs"],
        "composition": {
            "fxs": 1,
        },
    },
    "0x0b1be49dcb62d6cbc27e510361e910a8a30f37a9": {
        "categories": ["intermediate_term_bond"],
        "symbol": "vst-dpx-stability-pool",
        "DEFAULT_APR": 0.1,
        "tags": ["vst"],
        "composition": {
            "vst": 1,
        },
    },
    "0x59d72ddb29da32847a4665d08ffc8464a7185fae": {
        "categories": ["small_cap_us_stocks", "long_term_bond"],
        "symbol": "magic-weth-uniswap-v3",
        "defillama-APY-pool-id": "afb71713-9c2e-4717-a8a3-9f959b966e49",
        "tags": ["magic", "eth"],
        "composition": {
            "eth": 0.5,
            "magic": 0.5,
        },
    },
    "0xc2054a8c33bfce28de8af4af548c48915c455c13": {
        "categories": ["large_cap_us_stocks"],
        "symbol": "RDNT-platform-fee",
        "DEFAULT_APR": 0.5,
        "tags": ["rdnt"],
        "composition": {
            "rdnt": 0.5,
        },
    },
}
DEBANK_ADDRESS = {
    "0x76ba3ec5f5adbf1c58c91e86502232317eea72de": {
        "categories": ["large_cap_us_stocks", "long_term_bond"],
        "symbol": "radiant-eth-dLP",
        "defillama-APY-pool-id": "118281c6-3a4a-4324-b804-5664617df77d",
        "tags": ["rdnt", "eth"],
        "composition": {
            "eth": 0.2,
            "rdnt": 0.8,
        },
    },
    "0xb7e50106a5bd3cf21af210a755f9c8740890a8c9": {
        "categories": ["small_cap_us_stocks", "long_term_bond"],
        "symbol": "magic-weth-sushi-LP",
        "defillama-APY-pool-id": "afb71713-9c2e-4717-a8a3-9f959b966e49",
        "tags": ["magic", "eth"],
        "composition": {
            "eth": 0.5,
            "magic": 0.5,
        },
    },
    "0x5fbbef48ce0850e5a73bc3f4a6e903458b3c0af4": {
        "categories": ["large_cap_us_stocks", "long_term_bond"],
        "symbol": "weth-gmx-TJ-LP-arb",
        "DEFAULT_APR": 0,
        "tags": ["eth", "gmx"],
        "composition": {
            "eth": 0.5,
            "gmx": 0.5,
        },
    },
    "0xdf3e481a05f58c387af16867e9f5db7f931113c9": {
        "categories": ["gold", "long_term_bond", "intermediate_term_bond"],
        "symbol": "weth-usdt-TJ-LP-avax",
        "DEFAULT_APR": 0,
        "tags": ["eth", "usdt"],
        "composition": {
            "eth": 0.5,
            "usdt": 0.5,
        },
    },
    "0x127963a74c07f72d862f2bdc225226c3251bd117": {
        "categories": ["intermediate_term_bond"],
        "symbol": "Vesta-frax",
        "defillama-APY-pool-id": "ca8b6649-b825-41c7-8955-47b955b37bb0",
        "tags": ["vst", "frax"],
        "composition": {
            "vst": 0.5,
            "frax": 0.5,
        },
    },
    "0x673cf5ab7b44caac43c80de5b99a37ed5b3e4cc6": {
        "categories": ["intermediate_term_bond", "long_term_bond"],
        "symbol": "gDAI",
        "defillama-APY-pool-id": "15c3e528-2825-4ca4-804b-406e8b8e2ebd",
        "tags": ["gdai"],
        "composition": {
            "eth": 0.36,
            "udsc": 0.64,
        },
    },
    "0x4e971a87900b931ff39d1aad67697f49835400b6": {
        "categories": [
            "large_cap_us_stocks",
            "long_term_bond",
            "intermediate_term_bond",
            "gold",
        ],
        "symbol": "glp-arbitrum",
        "defillama-APY-pool-id": "825688c0-c694-4a6b-8497-177e425b7348",
        "tags": ["glp"],
        "composition": {
            "eth": 0.28,
            "wbtc": 0.2,
            "link": 0.01,
            "uni": 0.01,
            "usdc": 0.41,
            "usdt": 0.02,
            "dai": 0.05,
            "frax": 0.02,
        },
    },
    "0xf4d73326c13a4fc5fd7a064217e12780e9bd62c3": {
        "categories": ["gold", "long_term_bond", "intermediate_term_bond"],
        "symbol": "usdt-weth-sushi-LP",
        "defillama-APY-pool-id": "abe3c385-bde7-4350-9f35-2f574ad592d6",
        "tags": ["usdt", "eth"],
        "composition": {
            "eth": 0.5,
            "usdt": 0.5,
        },
    },
    "0xbdec4a045446f583dc564c0a227ffd475b329bf0": {
        "categories": ["gold", "long_term_bond", "intermediate_term_bond"],
        "symbol": "dai-weth-kyberswap-LP",
        "defillama-APY-pool-id": "592db49f-ac12-4072-b659-4e4a29c2b197",
        "tags": ["dai", "eth"],
        "composition": {
            "eth": 0.5,
            "dai": 0.5,
        },
    },
    "0x3d9819210a31b4961b30ef54be2aed79b9c9cd3b": {
        "categories": ["intermediate_term_bond"],
        "symbol": "compound USDT",
        "DEFAULT_APR": 0.02,
        "tags": ["cusdt"],
        "composition": {
            "usdt": 1,
        },
    },
    "0x41a5881c17185383e19df6fa4ec158a6f4851a69": {
        "categories": ["intermediate_term_bond"],
        "symbol": "cvxOHMFRAXBP-f",
        "defillama-APY-pool-id": "4f000353-5bb0-4e8c-ad03-194f0662680d",
        "tags": ["ohm", "frax", "usdc"],
        "composition": {
            "ohm": 0.5,
            "frax": 0.25,
            "usdc": 0.25,
        },
    },
    "0xf562b2f33b3c90d5d273f88cdf0ced866e17092e": {
        "categories": ["intermediate_term_bond"],
        "symbol": "FraxSwapOHM",
        "defillama-APY-pool-id": "41e4d018-b7df-422d-93af-d7d4ff94b300",
        "tags": ["frax", "ohm"],
        "composition": {
            "ohm": 0.5,
            "frax": 0.5,
        },
    },
    "0x4804357ace69330524ceb18f2a647c3c162e1f95": {
        "categories": ["non_us_developed_market_stocks", "commodities"],
        "symbol": "Mare-Kava-lending",
        "defillama-APY-pool-id": "d09a22df-779c-4917-b66f-9e57b2f379f6",
        "tags": ["kava"],
        "composition": {
            "kava": 1,
        },
    },
    "0xf4b1486dd74d07706052a33d31d7c0aafd0659e1": {
        "categories": ["long_term_bond"],
        "symbol": "Radiant-ETH-lending",
        "DEFAULT_APR": 0.14,
        "tags": ["eth"],
        "composition": {
            "eth": 1,
        },
    },
}
BINANCE_ADDRESS = {
    "0x0fa70bd9b892c7b6d2a9ea8dd1ce446e52f86935": {
        "categories": ["commodities"],
        "symbol": "FIL-stake",
        "DEFAULT_APR": 0.05,
        "tags": ["fil"],
        "composition": {
            "fil": 1,
        },
    }
}
NANSEN_ADDRESS = {
    "EA1D43981D5C9A1C4AAEA9C23BB1D4FA126BA9BC7020A25E0AE4AA841EA25DC5": {
        "categories": [
            "non_us_emerging_market_stocks",
            "long_term_bond",
            "commodities",
        ],
        "symbol": "OSMO/WETH",
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
            "commodities",
        ],
        "symbol": "OSMO/KAVA",
        "defillama-APY-pool-id": "f6efb5eb-b6fc-4ada-8fe2-05702f38d606",
        "tags": ["osmo", "kava"],
        "composition": {
            "kava": 0.5,
            "osmo": 0.5,
        },
    },
    "27394FB092D2ECCD56123C74F36E4C1F926001CEADA9CA97EA622B25F41E5EB2": {
        "categories": ["non_us_emerging_market_stocks", "commodities"],
        "symbol": "OSMO/ATOM",
        "defillama-APY-pool-id": "4ced8c2d-67c4-4555-b025-be49c110ca58",
        "tags": ["osmo", "atom"],
        "composition": {
            "atom": 0.5,
            "osmo": 0.5,
        },
    },
    "DEC41A02E47658D40FC71E5A35A9C807111F5A6662A3FB5DA84C4E6F53E616B3": {
        "categories": ["non_us_emerging_market_stocks", "commodities"],
        "symbol": "ATOM-stake",
        "DEFAULT_APR": 0.2,
        "tags": ["atom"],
        "composition": {
            "atom": 1,
        },
    },
}

ADDRESS_2_CATEGORY = {
    **ZAPPER_ADDRESS,
    **DEBANK_ADDRESS,
    **BINANCE_ADDRESS,
    **NANSEN_ADDRESS,
}

# TODO(david): use this one to implement advanced search algorithm. Search for new compositions.
TOKEN_2_CATEGORIES = {
    "long_term_bond": ["eth"],
    "intermediate_term_bond": ["ohm", "gohm", "usdc", "frax", "dai", "gdai"],
    "commodities": ["fil", "cvxcrv", "crv", "cvx", "kava", "atom"],
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
}

LIQUIDITY_BOOK_PROTOCOL_APR_DISCOUNT_FACTOR = {
    "uniswap-v3": 0.5,
    "kyberswap-elastic": 0.5,
}
