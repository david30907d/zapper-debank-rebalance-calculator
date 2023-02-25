from portfolio_config import ADDRESS_2_CATEGORY
from handlers.utils import mapping_table_checking_logic

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
                apr = ADDRESS_2_CATEGORY.get(asset_address, {}).get("APR", 0)
                # my sentry logic
                mapping_table_checking_logic(
                    asset_address, asset, asset["balanceUSD"], categories, apr
                )
                length_of_categories = len(categories)
                symbol = ADDRESS_2_CATEGORY.get(asset_address, {}).get("symbol", "")
                for category in categories:
                    weighted_balanceUSD = asset["balanceUSD"] / length_of_categories
                    result[category]["portfolio"][symbol][
                        "worth"
                    ] += weighted_balanceUSD
                    result[category]["portfolio"][symbol]["APR"] = apr
                    result[category]["sum"] += weighted_balanceUSD
    return result
