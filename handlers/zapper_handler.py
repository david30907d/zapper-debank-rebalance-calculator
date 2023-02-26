from portfolio_config import ADDRESS_2_CATEGORY
from handlers.utils import mapping_table_checking_logic
from apr_utils.apr_calculator import get_latest_apr
import json
def _zapper_handler(positions, result):
    for position in positions:
        if position["balanceUSD"] < 200:
            continue
        for product in position["products"]:
            for asset in product["assets"]:
                asset_address = (
                    asset["address"]
                    if not asset.get("dataProps", {}).get("poolAddress")
                    else asset.get("dataProps", {}).get("poolAddress")
                )
                categories = ADDRESS_2_CATEGORY.get(asset_address, {}).get(
                    "categories", []
                )
                symbol = ADDRESS_2_CATEGORY.get(asset_address, {}).get("symbol", "")
                if not categories and not symbol:
                    continue
                apr = get_latest_apr(symbol)
                length_of_categories = len(categories)
                for category in categories:
                    weighted_balanceUSD = asset["balanceUSD"] / length_of_categories
                    result[category]["portfolio"][symbol][
                        "worth"
                    ] += weighted_balanceUSD
                    result[category]["portfolio"][symbol]["APR"] = apr
                    result[category]["sum"] += weighted_balanceUSD
    return result
