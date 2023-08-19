import json

from rebalance_server.apr_utils import convert_apr_to_apy, convert_apy_to_apr
from rebalance_server.apr_utils.apr_calculator import get_apy, get_lowest_or_default_apr
from rebalance_server.portfolio_config import (
    BLACKLIST_CHAINS,
    BLACKLIST_CHAINS_FOR_STABLE_COIN,
    BLACKLIST_PROTOCOL,
    STABLE_COIN_WHITELIST,
)
from rebalance_server.search_handlers import SearchBase
from rebalance_server.search_handlers.jaccard_similarity_handler import (
    JaccardSimilarityHandler,
)
from rebalance_server.search_handlers.ngram_handler import NgramSimilarityHandler
from rebalance_server.utils.position import skip_rebalance_if_position_too_small

MILLION = 10**6


def search_better_stable_coin_pools(categorized_positions: dict, topn_int: int = 5):
    with open("rebalance_server/yield-llama.json", "r") as f:
        defillama = json.load(f)
    max_apy = _get_current_stable_max_apy_in_your_portfolio(
        categorized_positions, defillama
    )
    topn = _get_topn_apy_pool(defillama, max_apy)
    top_n_stable_coins = []
    for pool in sorted(topn, key=lambda x: x["apy"], reverse=True):
        if pool["tvlUsd"] < MILLION / 10:
            continue
        if pool["chain"] in BLACKLIST_CHAINS_FOR_STABLE_COIN:
            continue
        if not _check_if_symbol_consists_of_whitelist_coins(pool["symbol"]):
            continue
        if pool["project"] in BLACKLIST_PROTOCOL:
            continue
        top_n_stable_coins.append(pool)
    return top_n_stable_coins[:topn_int]


def search_top_n_pool_consist_of_same_lp_token(
    categorized_positions: dict, optimize_apr_mode: str
) -> list[dict]:
    print("\n\n=======Search top n pools consist of same lp token=======")
    res_json = json.load(open("rebalance_server/yield-llama.json", "r"))
    search_handler = _get_search_handler(
        optimize_apr_mode=optimize_apr_mode, searching_algorithm="jaccard_similarity"
    )
    project_symbol_set = set()
    pool_ids_of_current_portfolio = set(
        metadata["metadata"].get("defillama-APY-pool-id")
        for portfolio in categorized_positions.values()
        for metadata in portfolio["portfolio"].values()
    )
    top_n_list = []
    for portfolio in categorized_positions.values():
        for project_symbol, metadata in portfolio["portfolio"].items():
            if project_symbol in project_symbol_set:
                # since each token might have several properties, it might exists in different portfolio
                # but we only need to search once
                continue
            project_symbol_set.add(project_symbol)
            apr = get_lowest_or_default_apr(project_symbol, metadata["address"])
            top_n = _get_topn_candidate_pool(
                apr,
                metadata,
                res_json,
                search_handler,
                pool_ids_of_current_portfolio,
            )
            top_n_list.append((project_symbol, top_n, apr))
    return top_n_list


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
    topn_int: int = 5,
) -> list:
    worth = metadata["worth"]
    top_n: list[dict] = []
    for pool_metadata in res_json["data"]:
        if skip_rebalance_if_position_too_small(worth):
            continue
        if pool_metadata["chain"] in BLACKLIST_CHAINS:
            continue
        if pool_metadata["project"] in BLACKLIST_PROTOCOL:
            continue
        if (
            pool_similarity := search_handler.get_similarity(
                metadata, pool_metadata["symbol"].lower()
            )
            > search_handler.similarity_threshold
            and pool_metadata["pool"] not in pool_ids_of_current_portfolio
            and current_apr < convert_apy_to_apr(get_apy(pool_metadata))
            and pool_metadata["tvlUsd"] > MILLION * 0.7
        ):
            top_n.append(
                {"pool_metadata": pool_metadata, "pool_similarity": pool_similarity}
            )
    # TODO(david): use harmonic mean of tvl and apr to sort
    return sorted(top_n, key=lambda x: -get_apy(x["pool_metadata"]))[:topn_int]


def print_out_topn_candidate_pool(
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
            -convert_apy_to_apr(get_apy(x["pool_metadata"])),
        ),
    )[:n]:
        metadata = metadata_with_similarity["pool_metadata"]
        print(
            f" - Chain: {metadata['chain']}, Protocol: {metadata['project']+':'+metadata['poolMeta'] if metadata['poolMeta'] else metadata['project']}, Token: {metadata['symbol']}, lowest or default APR: {convert_apy_to_apr(get_apy(metadata)):.2f}"
        )


def _get_current_stable_max_apy_in_your_portfolio(
    categorized_positions: dict, defillama: dict
):
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
        for key in ["defillama-APY-pool-id", "DEFAULT_APR", "APR"]:
            potential_defillama_key = portfolio["metadata"].get(key)
            if potential_defillama_key is None:
                continue
            apy = 0
            if key == "defillama-APY-pool-id":
                if potential_defillama_key in defillama_APY_pool_id_to_apy:
                    apy = defillama_APY_pool_id_to_apy[potential_defillama_key]
            else:
                apy = convert_apr_to_apy(float(potential_defillama_key))
            if apy > max_apy:
                max_apy = apy
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


def show_topn_stable_coins(topn: list):
    # Code to display top N pools
    print("====================")
    print("Better stable coin:")
    print("Current Blacklist Chains: ", ", ".join(BLACKLIST_CHAINS_FOR_STABLE_COIN))
    print("Current Whitelist Stable Coins: ", ", ".join(STABLE_COIN_WHITELIST))
    for pool in sorted(topn, key=lambda x: x["apy"], reverse=True):
        print(
            f"- Chain: {pool['chain']}, Pool: {pool['project']}, Coin: {pool['symbol']}, TVL: {pool['tvlUsd']/MILLION:.2f}M, APR: {convert_apy_to_apr(pool['apy']/100)*100:.2f}%"
        )


def _check_if_symbol_consists_of_whitelist_coins(symbol: str):
    for subsymbol in symbol.split("-"):
        if subsymbol not in STABLE_COIN_WHITELIST:
            return False
    return True
