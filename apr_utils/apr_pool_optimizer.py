import json

import ngram

from apr_utils.apr_calculator import get_latest_apr
from apr_utils.utils import convert_apy_to_apr
from utils.position import skip_rebalance_if_position_too_small


def search_top_n_pool_consist_of_same_lp_token(
    categorized_positions: dict, optimize_apr_mode: str
) -> list[dict]:
    print("=======Search top n pools consist of same lp token=======")
    res_json = json.load(open("yield-llama.json", "r"))
    search_handler = _get_search_handler(
        optimize_apr_mode=optimize_apr_mode, searching_algorithm="ngram"
    )
    symbol_set = set()
    for portfolio in categorized_positions.values():
        for symbol, metadata in portfolio["portfolio"].items():
            if symbol in symbol_set:
                continue
            symbol_set.add(symbol)
            worth = metadata["worth"]
            top_n = []
            current_apr = get_latest_apr(symbol)
            for pool_metadata in res_json["data"]:
                if skip_rebalance_if_position_too_small(worth):
                    continue
                if (
                    search_handler(symbol, pool_metadata["symbol"])
                    and metadata["metadata"].get("defillama-APY-pool-id")
                    != pool_metadata["pool"]
                    and current_apr
                    < convert_apy_to_apr(pool_metadata["apyMean30d"] / 100)
                ):
                    top_n.append(pool_metadata)
            _print_out_topn_candidate_pool(symbol, top_n, current_apr)
    return top_n


def _get_search_handler(optimize_apr_mode: str, searching_algorithm: str):
    if optimize_apr_mode == "new_pool":
        if searching_algorithm == "ngram":
            threashold = 0.2
            return (
                lambda symbol, compared_symbol: ngram.NGram.compare(
                    symbol.lower(), compared_symbol.lower()
                )
                > threashold
            )
        raise NotImplementedError(
            f"search algorithm {searching_algorithm} not implemented"
        )
    elif optimize_apr_mode == "new_combination":
        raise NotImplementedError("Not implemented yet")


def _print_out_topn_candidate_pool(
    symbol: str, top_n: list, current_apr: float, n: int = 3
):
    if not top_n:
        return
    print(
        f"{symbol}'s possible better protocol to deposit (Current apyMean30d {current_apr:.2f}):"
    )
    for metadata in sorted(top_n, key=lambda x: -x["apyMean30d"])[:n]:
        print(
            f" - Chain: {metadata['chain']}, Protocol: {metadata['project']}, Token: {metadata['symbol']}, APR: {((metadata['apyMean30d']/100+1)**(1/365)-1)*365:.2f}"
        )
