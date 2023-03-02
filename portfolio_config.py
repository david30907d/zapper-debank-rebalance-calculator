MIN_REBALANCE_POSITION_THRESHOLD = 500
DEFILLAMA_API_REQUEST_FREQUENCY_RECIPROCAL = 40
ZAPPER_ADDRESS = {
    "0x8ec22ec81e740e0f9310e7318d03c494e62a70cd": {
        "categories": ["cash"],
        "symbol": "crvEURSUSD",
        "defillama-APY-pool-id": "9cf3f9d1-bc48-4436-8ef9-5ecf786c7a9b",
    },
    "0xd2d1162512f927a7e282ef43a362659e4f2a728f": {
        "categories": ["gold"],
        "symbol": "glp-avax",
        "defillama-APY-pool-id": "6a3ddb91-0638-4454-97c1-86dc6d59f32c",
    },
    "0xa14dbce13c22c97fd99daa0de3b1b480c7c3fdf6": {
        "categories": ["stock"],
        "symbol": "trader-joe-dpx-weth",
        "DEFAULT_APR": 0,
    },
    "0xf4d73326c13a4fc5fd7a064217e12780e9bd62c3": {
        "categories": ["stock"],
        "symbol": "magic-weth-sushi-LP",
        "defillama-APY-pool-id": "5f98842f-72cb-4579-807f-403ca2dfb993",
    },
    "0x4e971a87900b931ff39d1aad67697f49835400b6": {
        "categories": ["gold"],
        "symbol": "glp-arbitrum",
        "defillama-APY-pool-id": "825688c0-c694-4a6b-8497-177e425b7348",
    },
    "0x100ec08129e0fd59959df93a8b914944a3bbd5df": {
        "categories": ["bond"],
        "symbol": "gohm",
        "DEFAULT_APR": 0.07,
    },
    "0x127963a74c07f72d862f2bdc225226c3251bd117": {
        "categories": ["cash"],
        "symbol": "VSTFRAX-f",
        "defillama-APY-pool-id": "ca8b6649-b825-41c7-8955-47b955b37bb0",
    },
    "0x27a8c58e3de84280826d615d80ddb33930383fe9": {
        "categories": ["cash", "bond", "gold"],
        "symbol": "cvxOHMFRAXBP-f",
        "defillama-APY-pool-id": "4f000353-5bb0-4e8c-ad03-194f0662680d",
    },
    "0xc96e1a26264d965078bd01eaceb129a65c09ffe7": {
        "categories": ["cash", "bond", "gold"],
        "symbol": "stkcvxOHMFRAXBP-f-frax",
        "defillama-APY-pool-id": "4f000353-5bb0-4e8c-ad03-194f0662680d",
    },
    "0x72a19342e8f1838460ebfccef09f6585e32db86e": {
        "categories": ["stock"],
        "symbol": "CVX",
        "defillama-APY-pool-id": "777032e6-e815-4f44-90b4-abb98f0f9632",
    },
    "0xaa0c3f5f7dfd688c6e646f66cd2a6b66acdbe434": {
        "categories": ["stock"],
        "symbol": "cvxCRV",
        "defillama-APY-pool-id": "f1b831a9-7763-4bad-a64e-cafc86fdb7ec",
    },
    "0x188bed1968b795d5c9022f6a0bb5931ac4c18f00": {
        "categories": ["stock"],
        "symbol": "Yeti-JLP",
        "DEFAULT_APR": 0.8,
    },
    "0xf562b2f33b3c90d5d273f88cdf0ced866e17092e": {
        "categories": ["bond", "cash", "gold"],
        "symbol": "FraxSwapOHM",
        "defillama-APY-pool-id": "41e4d018-b7df-422d-93af-d7d4ff94b300",
    },
    "0xf650c3d88d12db855b8bf7d11be6c55a4e07dcc9": {
        "categories": ["cash"],
        "symbol": "compound USDT",
        "DEFAULT_APR": 0.02,
    },
    "0x8d9ba570d6cb60c7e3e0f31343efe75ab8e65fb1": {
        "categories": ["bond"],
        "symbol": "gohm-arb",
        "DEFAULT_APR": 0.07,
    },
    "0x0ab87046fbb341d058f17cbc4c1133f25a20a52f": {
        "categories": ["bond"],
        "symbol": "gohm",
        "DEFAULT_APR": 0.07,
    },
    "0x1f80c96ca521d7247a818a09b0b15c38e3e58a28": {
        # TODO: david to figure out weather dpx is stock or gold
        "categories": ["stock"],
        "symbol": "sushi-dpx-weth-LP",
        "defillama-APY-pool-id": "97cb382d-8dc4-4e17-b0f6-b6b51994dbeb",
    },
    "0x1701a7e5034ed1e35c52245ab7c07dbdaf353de7": {
        "categories": ["stock"],
        "symbol": "kyber-avax-eth-LP",
        "defillama-APY-pool-id": "ca1058be-6d4b-4dc2-97f9-cf09dae2a10e",
    },
    "0xb5c88537d8f5f356e43ec94e20f7eb26bd1ac967": {
        "categories": ["stock"],
        "symbol": "DPX-WETH",
        "defillama-APY-pool-id": "ce53d880-7ebf-40c5-9d97-e4c0fa0bc127",
    },
    "0xd85e038593d7a098614721eae955ec2022b9b91b": {
        "categories": ["cash"],
        "symbol": "gDAI",
        "defillama-APY-pool-id": "15c3e528-2825-4ca4-804b-406e8b8e2ebd",
    },
    "0x80789d252a288e93b01d82373d767d71a75d9f16": {
        "categories": ["stock"],
        "symbol": "veDPX",
        "DEFAULT_APR": 0.13,
    },
    "0xc8418af6358ffdda74e09ca9cc3fe03ca6adc5b0": {
        "categories": ["stock"],
        "symbol": "veFXS",
        "DEFAULT_APR": 0.01,
    },
}
DEBANK_ADDRESS = {
    "0xfffffffffff5d3627294fec5081ce5c5d7fa6451": {
        "categories": [
            "cash",
        ],
        "symbol": "YUSD",
        "DEFAULT_APR": 0.2,
    },
    "0xb5352a39c11a81fe6748993d586ec448a01f08b5": {
        "categories": ["cash", "stock", "gold"],
        "symbol": "avax-usdc-TJ-avax",
        "DEFAULT_APR": 0,
    },
    "0xc963ef7d977ecb0ab71d835c4cb1bf737f28d010": {
        "categories": ["stock"],
        "symbol": "radiant-eth-LP",
        "defillama-APY-pool-id": "118281c6-3a4a-4324-b804-5664617df77d",
    },
    "0xb7e50106a5bd3cf21af210a755f9c8740890a8c9": {
        "categories": ["stock"],
        "symbol": "magic-weth-sushi-LP",
        "defillama-APY-pool-id": "5f98842f-72cb-4579-807f-403ca2dfb993",
    },
    "0x7ec3717f70894f6d9ba0be00774610394ce006ee": {
        "categories": ["stock", "gold", "cash"],
        "symbol": "weth-usdc-TJ-LP",
        "DEFAULT_APR": 0,
    },
    "0x5fbbef48ce0850e5a73bc3f4a6e903458b3c0af4": {
        "categories": ["stock", "gold"],
        "symbol": "weth-gmx-TJ-LP-arb",
        "DEFAULT_APR": 0,
    },
    "0x42be75636374dfa0e57eb96fa7f68fe7fcdad8a3": {
        "categories": ["stock"],
        "symbol": "weth-avax-TJ-LP-avax",
        "DEFAULT_APR": 0,
    },
    "0xdf3e481a05f58c387af16867e9f5db7f931113c9": {
        "categories": ["stock", "cash", "gold"],
        "symbol": "weth-usdt-TJ-LP-avax",
        "DEFAULT_APR": 0,
    },
    "0x104f1459a2ffea528121759b238bb609034c2f01": {
        "categories": ["stock", "cash", "gold"],
        "symbol": "balancer-usdt-eth-btc-arb",
        "DEFAULT_APR": 0.15,
    },
    "0x5851e2d6396bcc26fb9eee21effbf99e0d2b2148": {
        "categories": ["stock", "cash", "gold"],
        "symbol": "weth-usdc-TJ-LP-avax",
        "DEFAULT_APR": 0,
    },
    "0xbdec4a045446f583dc564c0a227ffd475b329bf0": {
        "categories": ["stock"],
        "symbol": "kyber-avax-eth-LP",
        "defillama-APY-pool-id": "ca1058be-6d4b-4dc2-97f9-cf09dae2a10e",
    },
}

ADDRESS_2_CATEGORY = {**ZAPPER_ADDRESS, **DEBANK_ADDRESS}

TOKEN_CATEGORIES = {
    "bond": ["gohm", "ohm"],
    "cash": ["usdt", "usdc", "dai", "frax", "vst"],
    "stock": [
        "eth",
        "weth",
        "avax",
        "wavax",
        "atom",
        "rdnt",
        "cvx",
        "crv",
        "cvxcrv",
        "dpx",
    ],
    "gold": ["glp"],
}

ZAPPER_SYMBOL_2_COINGECKO_MAPPING = {"EURS": "stasis-eurs"}
