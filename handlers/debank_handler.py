from rebalance_server.apr_utils.apr_calculator import get_lowest_or_default_apr
from rebalance_server.handlers.utils import place_value_into_categorized_portfolio_dict
from rebalance_server.portfolio_config import (
    ADDRESS_2_CATEGORY,
    MIN_REBALANCE_POSITION_THRESHOLD,
    get_metadata_by_project_symbol,
)


def debank_handler(positions, result):
    for pool in positions["data"]["result"]["data"]:
        for portfolio in pool["portfolio_item_list"]:
            net_usd_valud = portfolio["stats"]["net_usd_value"]
            if net_usd_valud < MIN_REBALANCE_POSITION_THRESHOLD:
                continue
            addr = _get_correct_addr(portfolio)
            project_id = _get_project_id(portfolio)
            unique_id = f"{addr}:{project_id}"
            categories = ADDRESS_2_CATEGORY.get(unique_id, {}).get("categories", [])
            length_of_categories = len(categories)
            symbol = ADDRESS_2_CATEGORY.get(unique_id, {}).get("symbol", "")
            project_symbol = f"{project_id}:{symbol}"
            if not symbol:
                raise Exception(
                    f"Address {unique_id} no category, need to update your ADDRESS_2_CATEGORY, or update its APR"
                )
            apr = get_lowest_or_default_apr(project_symbol, unique_id)
            metadata = get_metadata_by_project_symbol(f"{project_id}:{symbol}")
            tokens_metadata = _get_token_metadata(portfolio)
            result = place_value_into_categorized_portfolio_dict(
                categories,
                net_usd_valud,
                length_of_categories,
                project_id,
                symbol,
                unique_id,
                apr,
                metadata,
                tokens_metadata,
                result,
            )
    return result


def _get_correct_addr(portfolio):
    return portfolio["pool"]["id"]


def _get_project_id(portfolio):
    return portfolio["pool"]["project_id"]


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
        for token in portfolio["detail"].get("supply_token_list", [])
    ]
    # rename amount to balance
    for token_metadata in token_metadatas:
        token_metadata["balance"] = token_metadata.pop("amount")
    return token_metadatas
