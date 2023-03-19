from apr_utils.apr_calculator import get_lowest_or_default_apr
from apr_utils.utils import get_metadata_by_symbol
from portfolio_config import ADDRESS_2_CATEGORY, MIN_REBALANCE_POSITION_THRESHOLD


def _debank_handler(positions, result):
    for pool in positions["data"]["result"]["data"]:
        for portfolio in pool["portfolio_item_list"]:
            net_usd_valud = portfolio["stats"]["net_usd_value"]
            if net_usd_valud < MIN_REBALANCE_POSITION_THRESHOLD:
                continue
            addr = _get_correct_addr(portfolio)
            categories = ADDRESS_2_CATEGORY.get(addr, {}).get("categories", [])
            length_of_categories = len(categories)
            symbol = ADDRESS_2_CATEGORY.get(addr, {}).get("symbol", "")
            if not symbol:
                raise Exception(
                    f"Address {addr} no category, need to update your ADDRESS_2_CATEGORY, or update its APR"
                )
            apr = get_lowest_or_default_apr(symbol)
            metadata = get_metadata_by_symbol(symbol)
            tokens_metadata = _get_token_metadata(portfolio)
            for category in categories:
                weighted_balanceUSD = net_usd_valud / length_of_categories
                result[category]["portfolio"][symbol]["worth"] += weighted_balanceUSD
                result[category]["portfolio"][symbol]["APR"] = apr
                result[category]["portfolio"][symbol]["metadata"] = metadata
                result[category]["portfolio"][symbol][
                    "tokens_metadata"
                ] = tokens_metadata
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


def _get_token_metadata(portfolio: dict):
    token_metadatas = [
        {
            k: v
            for k, v in token.items()
            if k
            in [
                "amount",
                "chain",
                "name",
                "optimized_symbol",
                "price",
                "protocol_id",
                "symbol",
            ]
        }
        for token in portfolio["detail"]["supply_token_list"]
    ]
    # rename amount to balance
    for token_metadata in token_metadatas:
        token_metadata["balance"] = token_metadata.pop("amount")
    return token_metadatas
