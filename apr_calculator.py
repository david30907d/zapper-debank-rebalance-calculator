import json, random, requests
from portfolio_config import ADDRESS_2_CATEGORY
def get_latest_apr(symbol, provider='defillama'):
    if provider == 'defillama':
        defillama_pool_uuid = _get_metadata_by_symbol(symbol).get('defillama-APY-pool-id', None)
        if not defillama_pool_uuid:
            return 0
        res_json = json.load(open('yield-llama.json', 'r'))
        if random.randint(0, 10) == 10:
            res = requests.get('https://yields.llama.fi/pools')
            res_json = res.json()
            json.dump(res_json, open('yield-llama.json', 'w'))
        for pool_metadata in res_json['data']:
            if pool_metadata['pool'] == defillama_pool_uuid:
                # turn APY back to APR
                return ((pool_metadata['apy']/100+1)**(1/365)-1)*365
        raise FileNotFoundError(f"Cannot find {defillama_pool_uuid} in defillama's API")
    else:
        raise NotImplementedError(f"Unknown provider: {provider}")

def _get_metadata_by_symbol(symbol: str) -> dict:
    for metadata in ADDRESS_2_CATEGORY.values():
        if metadata['symbol'] == symbol:
            return metadata
    raise Exception(f"Cannot find {symbol} in your address mapping table")

