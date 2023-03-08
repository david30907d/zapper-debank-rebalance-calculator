import json
import random

import requests

from apr_utils.utils import convert_apy_to_apr, get_metadata_by_symbol
from portfolio_config import (
    DEFILLAMA_API_REQUEST_FREQUENCY_RECIPROCAL,
    LIQUIDITY_BOOK_PROTOCOL_APR_DISCOUNT_FACTOR,
)


def get_latest_apr(symbol, provider="defillama"):
    if provider == "defillama":
        defillama_pool_uuid = get_metadata_by_symbol(symbol).get(
            "defillama-APY-pool-id", None
        )
        if not defillama_pool_uuid:
            default_apr = _get_default_apr(symbol)
            if default_apr:
                return default_apr
            raise Exception(f"{symbol}'s APR is 0, are you sure you want to continue?")
        try:
            res_json = json.load(open("yield-llama.json", "r"))
        except FileNotFoundError:
            res_json = _get_data_from_defillama()
        if random.randint(0, DEFILLAMA_API_REQUEST_FREQUENCY_RECIPROCAL) == 0:
            print(
                f"Update Defillama data from API (1/{DEFILLAMA_API_REQUEST_FREQUENCY_RECIPROCAL}) chance"
            )
            res_json = _get_data_from_defillama()
        for pool_metadata in res_json["data"]:
            if pool_metadata["pool"] == defillama_pool_uuid:
                lowest_apy = _get_lowest_apy(pool_metadata)
                protocol_apy = _lower_the_apy_if_protocol_uses_liquidity_book(
                    pool_metadata["project"], lowest_apy
                )
                return convert_apy_to_apr(protocol_apy / 100)
        raise FileNotFoundError(f"Cannot find {defillama_pool_uuid} in defillama's API")
    else:
        raise NotImplementedError(f"Unknown provider: {provider}")


def _get_data_from_defillama():
    res = requests.get("https://yields.llama.fi/pools")
    res_json = res.json()
    json.dump(res_json, open("yield-llama.json", "w"))
    return res_json


def _get_default_apr(symbol: str):
    return get_metadata_by_symbol(symbol).get("DEFAULT_APR", 0)


def _get_lowest_apy(pool_metadata):
    # use the lowest APY to calculate my revenue in case I spent too much money this month
    return (
        pool_metadata["apyMean30d"]
        if pool_metadata["apyMean30d"] < pool_metadata["apy"]
        else pool_metadata["apy"]
    )


def _lower_the_apy_if_protocol_uses_liquidity_book(project_name: str, apy: float):
    return apy * LIQUIDITY_BOOK_PROTOCOL_APR_DISCOUNT_FACTOR.get(project_name, 1)
