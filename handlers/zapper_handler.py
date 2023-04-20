from apr_utils.apr_calculator import get_lowest_or_default_apr
from apr_utils.utils import get_metadata_by_project_symbol
from handlers.utils import place_value_into_categorized_portfolio_dict
from portfolio_config import ADDRESS_2_CATEGORY, MIN_REBALANCE_POSITION_THRESHOLD


def zapper_handler(positions, result):
    for position in positions:
        if position["balanceUSD"] < MIN_REBALANCE_POSITION_THRESHOLD:
            continue
        for product in position["products"]:
            for asset in product["assets"]:
                asset_address = _get_correct_addr(asset)
                categories = ADDRESS_2_CATEGORY.get(asset_address, {}).get(
                    "categories", []
                )
                project = ADDRESS_2_CATEGORY[asset_address]["project"].lower()
                symbol = (
                    ADDRESS_2_CATEGORY.get(asset_address, {}).get("symbol", "").lower()
                )
                project_symbol = f"{project}:{symbol}"
                defillama_pool_uuid = ADDRESS_2_CATEGORY.get(asset_address, {}).get(
                    "defillama-APY-pool-id", ""
                )

                # sanity check
                if (
                    asset["balanceUSD"] > MIN_REBALANCE_POSITION_THRESHOLD
                    and not categories
                ):
                    raise Exception(
                        f"Address {asset_address} no category, need to update your ADDRESS_2_CATEGORY, or update its APR"
                    )
                elif not symbol and not categories:
                    continue
                apr = get_lowest_or_default_apr(project_symbol, defillama_pool_uuid)
                metadata = get_metadata_by_project_symbol(project_symbol)
                tokens_metadata = [
                    {
                        k: v
                        for k, v in token.items()
                        if k
                        in [
                            "metaType",
                            "type",
                            "appId",
                            "price",
                            "symbol",
                            "tokens",
                            "address",
                            "network",
                            "balance",
                            "balanceUSD",
                        ]
                    }
                    for token in asset["tokens"]
                    if token.get("metaType") == "supplied"
                ]
                length_of_categories = len(categories)
                net_usd_value = asset["balanceUSD"]
                result = place_value_into_categorized_portfolio_dict(
                    categories,
                    net_usd_value,
                    length_of_categories,
                    symbol,
                    apr,
                    metadata,
                    tokens_metadata,
                    result,
                )
    return result


def _get_correct_addr(asset: dict) -> str:
    poolAddress = asset.get("dataProps", {}).get("poolAddress")
    if poolAddress:
        return poolAddress
    for token in asset["tokens"]:
        if token.get("metaType") == "supplied" and token.get("type") == "app-token":
            return token["address"]
    return asset["address"]
