import json, random, requests
from apr_utils.utils import get_metadata_by_symbol, convert_apy_to_apr
def get_latest_apr(symbol, provider='defillama'):
    if provider == 'defillama':
        defillama_pool_uuid = get_metadata_by_symbol(symbol).get('defillama-APY-pool-id', None)
        if not defillama_pool_uuid:
            return 0
        res_json = json.load(open('yield-llama.json', 'r'))
        # if random.randint(0, 10) == 10:
        #     res = requests.get('https://yields.llama.fi/pools')
        #     res_json = res.json()
        #     json.dump(res_json, open('yield-llama.json', 'w'))
        for pool_metadata in res_json['data']:
            if pool_metadata['pool'] == defillama_pool_uuid:
                # turn APY back to APR
                return convert_apy_to_apr(pool_metadata['apy']/100)
        raise FileNotFoundError(f"Cannot find {defillama_pool_uuid} in defillama's API")
    else:
        raise NotImplementedError(f"Unknown provider: {provider}")