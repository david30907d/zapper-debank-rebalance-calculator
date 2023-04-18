import json

from apr_utils.apr_calculator import get_lowest_apy, get_lowest_or_default_apr
from apr_utils.utils import convert_apy_to_apr
from portfolio_config import BLACKLIST_CHAINS, BLACKLIST_COINS
from search_handlers import SearchBase
from search_handlers.jaccard_similarity_handler import JaccardSimilarityHandler
from search_handlers.ngram_handler import NgramSimilarityHandler
from utils.position import skip_rebalance_if_position_too_small

MILLION = 10**6


def search_better_stable_coin_pools(categorized_positions: dict):
    with open("yield-llama.json", "r") as f:
        defillama = json.load(f)
    max_apy = _get_max_apy(categorized_positions, defillama)
    topn = _get_topn_apy_pool(defillama, max_apy)
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
            apr = get_lowest_or_default_apr(symbol)
            top_n = _get_topn_candidate_pool(
                apr,
                metadata,
                res_json,
                search_handler,
                pool_ids_of_current_portfolio,
            )
            _print_out_topn_candidate_pool(symbol, top_n, apr)
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
    top_n: list[dict] = []
    for pool_metadata in res_json["data"]:
        if skip_rebalance_if_position_too_small(worth):
            continue
        if pool_metadata["chain"] in BLACKLIST_CHAINS:
            continue
        if (
            pool_similarity := search_handler.get_similarity(
                metadata, pool_metadata["symbol"].lower()
            )
            > search_handler.similarity_threshold
            and pool_metadata["pool"] not in pool_ids_of_current_portfolio
            and current_apr < convert_apy_to_apr(get_lowest_apy(pool_metadata))
            and pool_metadata["tvlUsd"] > MILLION
        ):
            top_n.append(
                {"pool_metadata": pool_metadata, "pool_similarity": pool_similarity}
            )
    return top_n


def _print_out_topn_candidate_pool(
    symbol: str, top_n: list, current_apr: float, n: int = 5
):
    if not top_n:
        return
    print(
        f"{symbol}'s possible better protocol to deposit (lowest or default apr {current_apr:.2f}):"
    )
    for metadata_with_similarity in sorted(
        top_n,
        key=lambda x: (
            -x["pool_similarity"],
            -convert_apy_to_apr(get_lowest_apy(x["pool_metadata"])),
        ),
    )[:n]:
        metadata = metadata_with_similarity["pool_metadata"]
        print(
            f" - Chain: {metadata['chain']}, Protocol: {metadata['project']+'-'+metadata['poolMeta'] if metadata['poolMeta'] else metadata['project']}, Token: {metadata['symbol']}, lowest or default APR: {convert_apy_to_apr(get_lowest_apy(metadata)):.2f}"
        )


def _get_max_apy(categorized_positions: dict, defillama: dict):
    """
    # Code to calculate the maximum APY for stable coin pools
    think of cash as intermediate_term_bond, since stable usd coin is actually a bond issued by US government
    """
    defillama_APY_pool_id_to_apy = {
        obj["pool"]: obj["apy"]
        for obj in defillama["data"]
        if obj["stablecoin"] is True
    }
    max_apy = 0
    for portfolio in categorized_positions["intermediate_term_bond"][
        "portfolio"
    ].values():
        defillama_APY_pool_id = portfolio["metadata"].get("defillama-APY-pool-id")
        if not defillama_APY_pool_id:
            continue
        if (
            defillama_APY_pool_id in defillama_APY_pool_id_to_apy
            and defillama_APY_pool_id_to_apy[defillama_APY_pool_id] > max_apy
        ):
            max_apy = defillama_APY_pool_id_to_apy[defillama_APY_pool_id]
    return max_apy


def _get_topn_apy_pool(defillama: dict, max_apy: float):
    # Code to retrieve top N pools with APYs greater than or equal to max_apy
    topn = []
    for pool in defillama["data"]:
        if (
            pool["stablecoin"] is True
            and pool["apy"] > max_apy
            and pool["apyMean30d"] > max_apy
        ):
            topn.append(pool)
    return topn


def _show_topn(topn: list):
    # Code to display top N pools
    print("====================")
    print("Better stable coin:")
    print("Current Blacklist Chains: ", ", ".join(BLACKLIST_CHAINS))
    print("Current Blacklist Coins: ", ", ".join(BLACKLIST_COINS))
    for pool in sorted(topn, key=lambda x: x["apy"], reverse=True):
        if pool["tvlUsd"] < MILLION:
            continue
        if pool["chain"] in BLACKLIST_CHAINS:
            continue

        if _check_if_symbol_has_blacklist_coins_substring(pool["symbol"]):
            continue
        print(
            f"- Chain: {pool['chain']}, Pool: {pool['project']}, Coin: {pool['symbol']}, TVL: {pool['tvlUsd']/MILLION:.2f}M, APR: {convert_apy_to_apr(pool['apy']/100)*100:.2f}%"
        )


def _check_if_symbol_has_blacklist_coins_substring(symbol: str):
    for blacklist_coin in BLACKLIST_COINS:
        if blacklist_coin in symbol:
            return True
    return False
