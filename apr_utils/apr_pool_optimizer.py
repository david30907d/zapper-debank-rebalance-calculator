import json

from apr_utils.apr_calculator import get_latest_apr
from apr_utils.utils import convert_apy_to_apr
from search_handlers import SearchBase
from search_handlers.jaccard_similarity_handler import JaccardSimilarityHandler
from search_handlers.ngram_handler import NgramSimilarityHandler
from utils.position import skip_rebalance_if_position_too_small

MILLION = 10**6


def search_better_stable_coin_pools(categorized_positions: dict):
    defillama = json.load(open("yield-llama.json", "r"))
    defillama_APY_pool_id_to_apy_base = {
        obj["pool"]: obj["apyBase"]
        for obj in defillama["data"]
        if obj["stablecoin"] is True and obj["apyBase"]
    }
    max_base_apr = _get_max_base_apy(
        categorized_positions, defillama_APY_pool_id_to_apy_base
    )
    topn = _get_topn_base_apr_pool(defillama, max_base_apr)
    _show_topn(topn)


def search_top_n_pool_consist_of_same_lp_token(
    categorized_positions: dict, optimize_apr_mode: str
) -> list[dict]:
    print("\n\n=======Search top n pools consist of same lp token=======")
    res_json = json.load(open("yield-llama.json", "r"))
    search_handler = _get_search_handler(
        optimize_apr_mode=optimize_apr_mode, searching_algorithm="jaccard_similarity"
    )
    symbol_set = set()
    pool_ids_of_current_portfolio = set(
        metadata["metadata"].get("defillama-APY-pool-id")
        for portfolio in categorized_positions.values()
        for metadata in portfolio["portfolio"].values()
    )
    for portfolio in categorized_positions.values():
        for symbol, metadata in portfolio["portfolio"].items():
            if symbol in symbol_set:
                # since each token might have several properties, it might exists in different portfolio
                # but we only need to search once
                continue
            symbol_set.add(symbol)
            current_apr = get_latest_apr(symbol)
            top_n = _get_topn_candidate_pool(
                current_apr,
                metadata,
                res_json,
                search_handler,
                pool_ids_of_current_portfolio,
            )
            _print_out_topn_candidate_pool(symbol, top_n, current_apr)
    print("\n")
    return top_n


def _get_search_handler(optimize_apr_mode: str, searching_algorithm: str):
    if optimize_apr_mode == "new_pool":
        if searching_algorithm == "ngram":
            # sucks
            threashold = 0.2
            return NgramSimilarityHandler(similarity_threshold=threashold)
        elif searching_algorithm == "jaccard_similarity":
            return JaccardSimilarityHandler(similarity_threshold=0.5)
    elif optimize_apr_mode == "new_combination":
        raise NotImplementedError("Not implemented yet")


def _get_topn_candidate_pool(
    current_apr: float,
    metadata: dict,
    res_json: dict,
    search_handler: SearchBase,
    pool_ids_of_current_portfolio: set,
) -> list:
    worth = metadata["worth"]
    top_n = []
    for pool_metadata in res_json["data"]:
        if skip_rebalance_if_position_too_small(worth):
            continue
        if (
            search_handler.check_similarity(metadata, pool_metadata["symbol"].lower())
            and pool_metadata["pool"] not in pool_ids_of_current_portfolio
            and current_apr < convert_apy_to_apr(pool_metadata["apyMean30d"] / 100)
            and pool_metadata["tvlUsd"] > MILLION
        ):
            top_n.append(pool_metadata)
    return top_n


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


def _get_max_base_apy(
    categorized_positions: dict, defillama_APY_pool_id_to_apy_base: dict
):
    max_base_apr = 0
    for portfolio in categorized_positions["cash"]["portfolio"].values():
        defillama_APY_pool_id = portfolio["metadata"].get("defillama-APY-pool-id")
        if not defillama_APY_pool_id:
            continue
        if (
            defillama_APY_pool_id in defillama_APY_pool_id_to_apy_base
            and defillama_APY_pool_id_to_apy_base[defillama_APY_pool_id] > max_base_apr
        ):
            max_base_apr = defillama_APY_pool_id_to_apy_base[defillama_APY_pool_id]
    return max_base_apr


def _get_topn_base_apr_pool(defillama: dict, max_base_apr: float):
    topn = []
    for pool in defillama["data"]:
        if (
            pool["stablecoin"] is True
            and pool["apyBase"] is not None
            and pool["apyBase"] > max_base_apr
            and pool["apyMean30d"] > max_base_apr
        ):
            topn.append(pool)
    return topn


def _show_topn(topn: list):
    print("====================")
    print("Better stable coin:")
    for pool in sorted(topn, key=lambda x: x["apyBase"], reverse=True):
        if pool["tvlUsd"] < MILLION:
            continue
        print(
            f"- Chain: {pool['chain']}, Pool: {pool['project']}, Coin: {pool['symbol']}, TVL: {pool['tvlUsd']/MILLION:.2f}M, Base APY: {pool['apyBase']:.2f}%,%"
        )
