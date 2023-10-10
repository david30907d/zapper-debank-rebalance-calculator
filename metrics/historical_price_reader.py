import json
import pathlib
import random

import numpy as np
import pandas as pd
import requests

from rebalance_server.metrics.utils import (
    FOUR_YEARS_AGO_UNIX_TIMESTAMP,
    TODAY_UNIX_TIMESTAMP,
)
from rebalance_server.portfolio_config import (
    DEBANK_SYMBOL_2_COINGECKO_MAPPING,
    DEFILLAMA_API_REQUEST_FREQUENCY_RECIPROCAL,
)


def get_historical_price_reader(source: str):
    if source == "coingecko":
        return CoinGeckoHistoricalPriceReader()
    else:
        raise NotImplementedError


class CoinGeckoHistoricalPriceReader:
    @staticmethod
    def get_token_historical_price(
        symbol: str,
    ) -> pd.Series:
        if (
            random.randint(0, DEFILLAMA_API_REQUEST_FREQUENCY_RECIPROCAL) == 0
            or not pathlib.Path(f"./rebalance_server/coingecko/{symbol}.json").exists()
        ):
            print(f"Update historical price data from CoinGecko: {symbol}...")
            res = requests.get(
                f"https://api.coingecko.com/api/v3/coins/{symbol}/market_chart/range?vs_currency=usd&from={FOUR_YEARS_AGO_UNIX_TIMESTAMP}&to={TODAY_UNIX_TIMESTAMP})"
            )
            if res.status_code == 200:
                json.dump(
                    res.json(), open(f"./rebalance_server/coingecko/{symbol}.json", "w")
                )
                res_json = res.json()
            else:
                print(res.json())
                res_json = json.load(
                    open(f"./rebalance_server/coingecko/{symbol}.json", "r")
                )
        else:
            res_json = json.load(
                open(f"./rebalance_server/coingecko/{symbol}.json", "r")
            )
        # use reverse to make the array' date in descending order
        # then trimming with different kind of tokens would be fine
        price = np.array(list(reversed(res_json["prices"])))[:, 1]
        return pd.Series(price)

    @staticmethod
    def convert_symbol_from_dashboard_to_api_version(symbol: str) -> str:
        return DEBANK_SYMBOL_2_COINGECKO_MAPPING[symbol]
