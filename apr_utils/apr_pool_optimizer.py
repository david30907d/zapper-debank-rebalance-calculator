import json
import ngram
from apr_utils.utils import get_metadata_by_symbol
from apr_utils.utils import convert_apy_to_apr
from apr_utils.apr_calculator import get_latest_apr

def search_top_n_pool_consist_of_same_lp_token(categorized_positions: dict) -> list[dict]:
    res_json = json.load(open('yield-llama.json', 'r'))
    search_handler = _get_search_handler('ngram')
    print(json.dumps(categorized_positions))
    for portfolio in categorized_positions.values():
        for symbol in portfolio["portfolio"].keys():
            top_n = []
            current_apr = get_latest_apr(symbol)
            for pool_metadata in res_json['data']:
                if search_handler(symbol, pool_metadata['symbol']) and get_metadata_by_symbol(symbol).get('defillama-APY-pool-id', None) != pool_metadata['pool'] and current_apr < convert_apy_to_apr(pool_metadata['apy']/100):
                    top_n.append(pool_metadata)
            _print_out_topn_candidate_pool(symbol, top_n)
    return top_n

def _get_search_handler(searching_algorithm):
    if searching_algorithm == 'ngram':
        threashold = 0.2
        return lambda symbol, compared_symbol: ngram.NGram.compare(symbol, compared_symbol) > threashold
    else:
        raise NotImplementedError(f"search algorithm {searching_algorithm} not implemented")

def _print_out_topn_candidate_pool(symbol: str, top_n: list, n: int=3):
    if not top_n:
        return
    print(f"{symbol}'s possible better protocol to deposit:")
    for metadata in sorted(top_n, key=lambda x: -x['apy'])[:n]:
        print(f" - Chain: {metadata['chain']}, Protocol: {metadata['project']}, Token: {metadata['symbol']}, APR: {((metadata['apy']/100+1)**(1/365)-1)*365:.2f}")