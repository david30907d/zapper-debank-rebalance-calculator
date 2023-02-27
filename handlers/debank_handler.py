from apr_utils.apr_calculator import get_latest_apr
from apr_utils.utils import get_metadata_by_symbol
from portfolio_config import ADDRESS_2_CATEGORY


def _debank_handler(positions, result):
    for pool in positions["data"]["result"]["data"]:
        for portfolio in pool["portfolio_item_list"]:
            addr = _get_correct_addr(portfolio)
            categories = ADDRESS_2_CATEGORY.get(addr, {}).get("categories", [])
            length_of_categories = len(categories)
            symbol = ADDRESS_2_CATEGORY.get(addr, {}).get("symbol", "")
            apr = get_latest_apr(symbol)
            metadata = get_metadata_by_symbol(symbol)
            for category in categories:
                weighted_balanceUSD = (
                    portfolio["stats"]["net_usd_value"] / length_of_categories
                )
                result[category]["portfolio"][symbol]["worth"] += weighted_balanceUSD
                result[category]["portfolio"][symbol]["APR"] = apr
                result[category]["portfolio"][symbol]["metadata"] = metadata
                result[category]["sum"] += weighted_balanceUSD
    return result


def _get_correct_addr(portfolio):
    addr = (
        portfolio["pool"]["id"]
        if len(portfolio["pool"]["id"].split(":")) == 1
        else portfolio["pool"]["id"].split(":")[1]
    )
    if len(addr) != 42:
        # TODO: use a function to handle
        addr = portfolio["pool"]["controller"]
    return addr
