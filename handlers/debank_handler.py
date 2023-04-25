from rebalance_server.apr_utils.apr_calculator import get_lowest_or_default_apr
from rebalance_server.apr_utils.utils import get_metadata_by_project_symbol
from rebalance_server.handlers.utils import place_value_into_categorized_portfolio_dict
from rebalance_server.portfolio_config import (
    ADDRESS_2_CATEGORY,
    MIN_REBALANCE_POSITION_THRESHOLD,
)


def debank_handler(positions, result):
    for pool in positions["data"]["result"]["data"]:
        for portfolio in pool["portfolio_item_list"]:
            net_usd_valud = portfolio["stats"]["net_usd_value"]
            if net_usd_valud < MIN_REBALANCE_POSITION_THRESHOLD:
                continue
            addr = _get_correct_addr(portfolio)
            categories = ADDRESS_2_CATEGORY.get(addr, {}).get("categories", [])
            length_of_categories = len(categories)
            project = ADDRESS_2_CATEGORY.get(addr, {}).get("project", "")
            symbol = ADDRESS_2_CATEGORY.get(addr, {}).get("symbol", "")
            project_symbol = f"{project}:{symbol}"
            if not symbol:
                raise Exception(
                    f"Address {addr} no category, need to update your ADDRESS_2_CATEGORY, or update its APR"
                )
            defillama_pool_uuid = ADDRESS_2_CATEGORY.get(addr, {}).get(
                "defillama-APY-pool-id", ""
            )
            apr = get_lowest_or_default_apr(project_symbol, defillama_pool_uuid)
            metadata = get_metadata_by_project_symbol(f"{project}:{symbol}")
            tokens_metadata = _get_token_metadata(portfolio)
            result = place_value_into_categorized_portfolio_dict(
                categories,
                net_usd_valud,
                length_of_categories,
                project,
                symbol,
                apr,
                metadata,
                tokens_metadata,
                result,
            )
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
