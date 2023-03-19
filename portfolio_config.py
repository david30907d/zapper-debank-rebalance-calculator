MIN_REBALANCE_POSITION_THRESHOLD = 500
DEFILLAMA_API_REQUEST_FREQUENCY_RECIPROCAL = 30
ZAPPER_ADDRESS = {
    "0x8ec22ec81e740e0f9310e7318d03c494e62a70cd": {
        "categories": ["cash"],
        "symbol": "crvEURSUSD",
        "defillama-APY-pool-id": "9cf3f9d1-bc48-4436-8ef9-5ecf786c7a9b",
        "tags": ["eurs", "usdt", "usdc"],
    },
    "0xd2d1162512f927a7e282ef43a362659e4f2a728f": {
        "categories": ["gold"],
        "symbol": "glp-avax",
        "defillama-APY-pool-id": "6a3ddb91-0638-4454-97c1-86dc6d59f32c",
        "tags": ["glp"],
    },
    "0xa14dbce13c22c97fd99daa0de3b1b480c7c3fdf6": {
        "categories": ["stock"],
        "symbol": "trader-joe-dpx-weth",
        "DEFAULT_APR": 0,
        "tags": ["dpx", "eth"],
    },
    "0xcb0e5bfa72bbb4d16ab5aa0c60601c438f04b4ad": {
        "categories": ["stock", "gold", "cash"],
        "symbol": "usdt-weth-sushi-LP",
        "defillama-APY-pool-id": "abe3c385-bde7-4350-9f35-2f574ad592d6",
        "tags": ["usdt", "eth"],
    },
    "0x4277f8f2c384827b5273592ff7cebd9f2c1ac258": {
        "categories": ["gold"],
        "symbol": "glp-arbitrum",
        "defillama-APY-pool-id": "825688c0-c694-4a6b-8497-177e425b7348",
        "tags": ["glp"],
    },
    "0x100ec08129e0fd59959df93a8b914944a3bbd5df": {
        "categories": ["bond"],
        "symbol": "gohm",
        "DEFAULT_APR": 0.07,
        "tags": ["gohm"],
    },
    "0x59bf0545fca0e5ad48e13da269facd2e8c886ba4": {
        "categories": ["cash"],
        "symbol": "VSTFRAX-f",
        "defillama-APY-pool-id": "ca8b6649-b825-41c7-8955-47b955b37bb0",
        "tags": ["vst", "frax"],
    },
    "0x81b0dcda53482a2ea9eb496342dc787643323e95": {
        "categories": ["cash", "bond", "gold"],
        "symbol": "cvxOHMFRAXBP-f",
        "defillama-APY-pool-id": "4f000353-5bb0-4e8c-ad03-194f0662680d",
        "tags": ["ohm", "frax", "usdc"],
    },
    "0xc96e1a26264d965078bd01eaceb129a65c09ffe7": {
        "categories": ["cash", "bond", "gold"],
        "symbol": "stkcvxOHMFRAXBP-f-frax",
        "defillama-APY-pool-id": "4f000353-5bb0-4e8c-ad03-194f0662680d",
        "tags": ["ohm", "frax", "usdc"],
    },
    "0x72a19342e8f1838460ebfccef09f6585e32db86e": {
        "categories": ["stock"],
        "symbol": "CVX",
        "defillama-APY-pool-id": "777032e6-e815-4f44-90b4-abb98f0f9632",
        "tags": [
            "cvx",
        ],
    },
    "0xaa0c3f5f7dfd688c6e646f66cd2a6b66acdbe434": {
        "categories": ["stock"],
        "symbol": "cvxCRV",
        "defillama-APY-pool-id": "f1b831a9-7763-4bad-a64e-cafc86fdb7ec",
        "tags": ["cvxcrv"],
    },
    "0x188bed1968b795d5c9022f6a0bb5931ac4c18f00": {
        "categories": ["stock"],
        "symbol": "Yeti-JLP",
        "DEFAULT_APR": 0.8,
    },
    "0x5769071665eb8db80e7e9226f92336bb2897dcfa": {
        "categories": ["bond", "cash", "gold"],
        "symbol": "FraxSwapOHM",
        "defillama-APY-pool-id": "41e4d018-b7df-422d-93af-d7d4ff94b300",
        "tags": ["frax", "ohm"],
    },
    "0xf650c3d88d12db855b8bf7d11be6c55a4e07dcc9": {
        "categories": ["cash"],
        "symbol": "compound USDT",
        "DEFAULT_APR": 0.02,
        "tags": ["cusdt"],
    },
    "0x8d9ba570d6cb60c7e3e0f31343efe75ab8e65fb1": {
        "categories": ["bond"],
        "symbol": "gohm-arb",
        "DEFAULT_APR": 0.07,
        "tags": ["gohm"],
    },
    "0x0ab87046fbb341d058f17cbc4c1133f25a20a52f": {
        "categories": ["bond"],
        "symbol": "gohm",
        "DEFAULT_APR": 0.07,
        "tags": ["gohm"],
    },
    "0x1f80c96ca521d7247a818a09b0b15c38e3e58a28": {
        # TODO: david to figure out weather dpx is stock or gold
        "categories": ["stock"],
        "symbol": "dopex-dpx-weth-LP",
        "defillama-APY-pool-id": "97cb382d-8dc4-4e17-b0f6-b6b51994dbeb",
        "tags": ["dpx", "eth"],
    },
    "0x1701a7e5034ed1e35c52245ab7c07dbdaf353de7": {
        "categories": ["stock", "gold"],
        "symbol": "kyber-avax-eth-LP",
        "defillama-APY-pool-id": "ca1058be-6d4b-4dc2-97f9-cf09dae2a10e",
        "tags": ["avax", "eth"],
    },
    "0xb5c88537d8f5f356e43ec94e20f7eb26bd1ac967": {
        "categories": ["stock"],
        "symbol": "sushi-DPX-WETH",
        "defillama-APY-pool-id": "97cb382d-8dc4-4e17-b0f6-b6b51994dbeb",
        "tags": ["dpx", "eth"],
    },
    "0xb52781c275431bd48d290a4318e338fe0df89eb9": {
        "categories": ["stock"],
        "symbol": "uniswap-DPX-WETH",
        "defillama-APY-pool-id": "ce53d880-7ebf-40c5-9d97-e4c0fa0bc127",
        "tags": ["dpx", "eth"],
    },
    "0xd85e038593d7a098614721eae955ec2022b9b91b": {
        "categories": ["cash"],
        "symbol": "gDAI",
        "defillama-APY-pool-id": "15c3e528-2825-4ca4-804b-406e8b8e2ebd",
        "tags": ["gdai"],
    },
    "0x80789d252a288e93b01d82373d767d71a75d9f16": {
        "categories": ["stock"],
        "symbol": "veDPX",
        "DEFAULT_APR": 0.13,
        "tags": ["vedpx"],
    },
    "0xc8418af6358ffdda74e09ca9cc3fe03ca6adc5b0": {
        "categories": ["stock"],
        "symbol": "veFXS",
        "DEFAULT_APR": 0.01,
        "tags": ["vefxs"],
    },
    "0x0b1be49dcb62d6cbc27e510361e910a8a30f37a9": {
        "categories": ["cash"],
        "symbol": "vst-dpx-stability-pool",
        "DEFAULT_APR": 0.1,
        "tags": ["vst"],
    },
    "0x59d72ddb29da32847a4665d08ffc8464a7185fae": {
        "categories": ["stock"],
        "symbol": "magic-weth-uniswap-v3",
        "defillama-APY-pool-id": "afb71713-9c2e-4717-a8a3-9f959b966e49",
        "tags": ["magic", "eth"],
    },
    "0xc2054a8c33bfce28de8af4af548c48915c455c13": {
        "categories": ["stock"],
        "symbol": "RDNT-platform-fee",
        "DEFAULT_APR": 0.5,
        "tags": ["rdnt"],
    },
}
DEBANK_ADDRESS = {
    "0xfffffffffff5d3627294fec5081ce5c5d7fa6451": {
        "categories": [
            "cash",
        ],
        "symbol": "YUSD",
        "DEFAULT_APR": 0.2,
        "tags": ["yusd"],
    },
    "0xb5352a39c11a81fe6748993d586ec448a01f08b5": {
        "categories": ["cash", "stock", "gold"],
        "symbol": "avax-usdc-TJ-avax",
        "DEFAULT_APR": 0,
        "tags": ["avax", "usdc"],
    },
    "0x24704aff49645d32655a76df6d407e02d146dafc": {
        "categories": ["stock"],
        "symbol": "radiant-eth-LP",
        "defillama-APY-pool-id": "118281c6-3a4a-4324-b804-5664617df77d",
        "tags": ["rdnt", "eth"],
    },
    "0xb7e50106a5bd3cf21af210a755f9c8740890a8c9": {
        "categories": ["stock"],
        "symbol": "magic-weth-sushi-LP",
        "defillama-APY-pool-id": "afb71713-9c2e-4717-a8a3-9f959b966e49",
        "tags": ["magic", "eth"],
    },
    "0x7ec3717f70894f6d9ba0be00774610394ce006ee": {
        "categories": ["stock", "gold", "cash"],
        "symbol": "weth-usdc-TJ-LP",
        "DEFAULT_APR": 0,
        "tags": ["usdc", "eth"],
    },
    "0x5fbbef48ce0850e5a73bc3f4a6e903458b3c0af4": {
        "categories": ["stock", "gold"],
        "symbol": "weth-gmx-TJ-LP-arb",
        "DEFAULT_APR": 0,
        "tags": ["eth", "gmx"],
    },
    "0x42be75636374dfa0e57eb96fa7f68fe7fcdad8a3": {
        "categories": ["stock"],
        "symbol": "weth-avax-TJ-LP-avax",
        "DEFAULT_APR": 0,
        "tags": ["eth", "avax"],
    },
    "0xdf3e481a05f58c387af16867e9f5db7f931113c9": {
        "categories": ["stock", "cash", "gold"],
        "symbol": "weth-usdt-TJ-LP-avax",
        "DEFAULT_APR": 0,
        "tags": ["eth", "usdt"],
    },
    "0x104f1459a2ffea528121759b238bb609034c2f01": {
        "categories": ["stock", "cash", "gold"],
        "symbol": "balancer-usdt-eth-btc-arb",
        "DEFAULT_APR": 0.15,
        "tags": ["eth", "usdt", "btc"],
    },
    "0x5851e2d6396bcc26fb9eee21effbf99e0d2b2148": {
        "categories": ["stock", "cash", "gold"],
        "symbol": "weth-usdc-TJ-LP-avax",
        "DEFAULT_APR": 0,
        "tags": ["eth", "usdc"],
    },
    "0xbdec4a045446f583dc564c0a227ffd475b329bf0": {
        "categories": ["stock"],
        "symbol": "kyber-avax-eth-LP",
        "defillama-APY-pool-id": "ca1058be-6d4b-4dc2-97f9-cf09dae2a10e",
        "tags": ["eth", "avax"],
    },
    "0x127963a74c07f72d862f2bdc225226c3251bd117": {
        "categories": ["cash"],
        "symbol": "Vesta-frax",
        "defillama-APY-pool-id": "ca8b6649-b825-41c7-8955-47b955b37bb0",
        "tags": ["vst", "avax"],
    },
    "0x673cf5ab7b44caac43c80de5b99a37ed5b3e4cc6": {
        "categories": ["cash"],
        "symbol": "gDAI",
        "defillama-APY-pool-id": "15c3e528-2825-4ca4-804b-406e8b8e2ebd",
        "tags": ["gdai"],
    },
    "0x4e971a87900b931ff39d1aad67697f49835400b6": {
        "categories": ["gold"],
        "symbol": "glp-arbitrum",
        "defillama-APY-pool-id": "825688c0-c694-4a6b-8497-177e425b7348",
        "tags": ["glp"],
    },
    "0xf4d73326c13a4fc5fd7a064217e12780e9bd62c3": {
        "categories": ["stock", "gold", "cash"],
        "symbol": "usdt-weth-sushi-LP",
        "defillama-APY-pool-id": "abe3c385-bde7-4350-9f35-2f574ad592d6",
        "tags": ["usdt", "eth"],
    },
    "0x3d9819210a31b4961b30ef54be2aed79b9c9cd3b": {
        "categories": ["cash"],
        "symbol": "compound USDT",
        "DEFAULT_APR": 0.02,
        "tags": ["cusdt"],
    },
    "0x41a5881c17185383e19df6fa4ec158a6f4851a69": {
        "categories": ["cash", "bond", "gold"],
        "symbol": "cvxOHMFRAXBP-f",
        "defillama-APY-pool-id": "4f000353-5bb0-4e8c-ad03-194f0662680d",
        "tags": ["ohm", "frax", "usdc"],
    },
    "0xf562b2f33b3c90d5d273f88cdf0ced866e17092e": {
        "categories": ["bond", "cash", "gold"],
        "symbol": "FraxSwapOHM",
        "defillama-APY-pool-id": "41e4d018-b7df-422d-93af-d7d4ff94b300",
        "tags": ["frax", "ohm"],
    },
    "0x4804357ace69330524ceb18f2a647c3c162e1f95": {
        "categories": ["stock"],
        "symbol": "Mare-Kava-lending",
        "defillama-APY-pool-id": "d09a22df-779c-4917-b66f-9e57b2f379f6",
        "tags": ["kava"],
    },
}

ADDRESS_2_CATEGORY = {**ZAPPER_ADDRESS, **DEBANK_ADDRESS}

# TODO(david): use this one to implement advanced search algorithm. Search for new compositions.
TOKEN_CATEGORIES = {
    "bond": ["eth", "weth"],
    "cash": ["gohm", "ohm"],
    "stock": ["eth", "weth", "atom", "rdnt", "cvx", "crv", "cvxcrv", "dpx", "kava"],
    "gold": ["glp"],
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
}

LIQUIDITY_BOOK_PROTOCOL_APR_DISCOUNT_FACTOR = {"uniswap-v3": 0.5}
