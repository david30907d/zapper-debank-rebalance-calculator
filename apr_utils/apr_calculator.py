import json
import random

import requests

from rebalance_server.apr_utils import convert_apy_to_apr
from rebalance_server.portfolio_config import (
    ADDRESS_2_CATEGORY,
    DEFILLAMA_API_REQUEST_FREQUENCY_RECIPROCAL,
    LIQUIDITY_BOOK_PROTOCOL_APR_DISCOUNT_FACTOR,
)
from rebalance_server.utils.position import get_metadata_by_project_symbol


def get_lowest_or_default_apr(project_symbol: str, addr: str):
    apr = ADDRESS_2_CATEGORY.get(addr, {}).get("APR")
    if apr is not None:
        return apr
    default_apr = _get_default_apr(project_symbol)
    if default_apr != 0:
        return default_apr
    defillama_pool_uuid = ADDRESS_2_CATEGORY.get(addr, {}).get(
        "defillama-APY-pool-id", ""
    )
    if defillama_pool_uuid:
        try:
            res_json = json.load(open("rebalance_server/yield-llama.json", "r"))
        except FileNotFoundError:
            res_json = _get_data_from_defillama()
        if random.randint(0, DEFILLAMA_API_REQUEST_FREQUENCY_RECIPROCAL) == 0:
            print(
                f"Update Defillama data from API (1/{DEFILLAMA_API_REQUEST_FREQUENCY_RECIPROCAL}) chance"
            )
            res_json = _get_data_from_defillama()
        for pool_metadata in res_json["data"]:
            if pool_metadata["pool"] == defillama_pool_uuid:
                protocol_apy = get_apy(pool_metadata)
                return convert_apy_to_apr(protocol_apy)
        raise FileNotFoundError(f"Cannot find {defillama_pool_uuid} in defillama's API")
    raise NotImplementedError(f"No APR for {project_symbol} and {addr}")


def _get_data_from_defillama():
    res = requests.get("https://yields.llama.fi/pools")
    res_json = res.json()
    json.dump(res_json, open("rebalance_server/yield-llama.json", "w"))
    return res_json


def _get_default_apr(project_symbol: str):
    return get_metadata_by_project_symbol(project_symbol).get("DEFAULT_APR", 0)


def get_apy(pool_metadata):
    # use the lowest APY to calculate my revenue in case I spent too much money this month
    apy = pool_metadata["apy"] / 100
    return _lower_the_apy_if_protocol_uses_liquidity_book(pool_metadata["project"], apy)


def _lower_the_apy_if_protocol_uses_liquidity_book(project_name: str, apy: float):
    return apy * LIQUIDITY_BOOK_PROTOCOL_APR_DISCOUNT_FACTOR.get(project_name, 1)
