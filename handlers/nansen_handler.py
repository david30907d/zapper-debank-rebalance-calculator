from rebalance_server.apr_utils.apr_calculator import get_lowest_or_default_apr
from rebalance_server.handlers.utils import place_value_into_categorized_portfolio_dict
from rebalance_server.portfolio_config import (
    ADDRESS_2_CATEGORY,
    MIN_REBALANCE_POSITION_THRESHOLD,
)
from rebalance_server.utils.position import get_metadata_by_project_symbol


def nansen_handler(positions, result):
    if "farms" in positions:
        return _nansen_farm_handler(positions, result)
    elif "delegation" in positions:
        return _nansen_stake_handler(positions, result)


def _nansen_farm_handler(positions, result):
    for farm in positions["farms"]:
        addr = _get_correct_addr(farm, address_column="tokens")
        net_usd_value = _calculate_net_usd_valud(farm)
        # sanity check
        if net_usd_value < MIN_REBALANCE_POSITION_THRESHOLD:
            continue
        categories = ADDRESS_2_CATEGORY[addr]["categories"]
        project = ADDRESS_2_CATEGORY[addr]["project"].lower()
        symbol = ADDRESS_2_CATEGORY[addr]["symbol"].lower()
        project_symbol = f"{project}:{symbol}"

        length_of_categories = len(categories)
        apr = get_lowest_or_default_apr(project_symbol, addr)
        metadata = get_metadata_by_project_symbol(project_symbol)
        tokens_metadata = _get_token_metadata(farm)
        result = place_value_into_categorized_portfolio_dict(
            categories,
            net_usd_value,
            length_of_categories,
            project,
            symbol,
            addr,
            apr,
            metadata,
            tokens_metadata,
            result,
        )
    return result


def _nansen_stake_handler(positions, result):
    for farm in positions["delegation"]:
        addr = _get_correct_addr(farm, address_column="rewards")
        net_usd_value = _calculate_net_usd_valud(farm)
        categories = ADDRESS_2_CATEGORY[addr]["categories"]
        project = ADDRESS_2_CATEGORY[addr]["project"].lower()
        symbol = ADDRESS_2_CATEGORY[addr]["symbol"].lower()
        project_symbol = f"{project}:{symbol}"
        defillama_pool_uuid = ADDRESS_2_CATEGORY.get(addr, {}).get(
            "defillama-APY-pool-id", ""
        )

        length_of_categories = len(categories)
        apr = get_lowest_or_default_apr(project_symbol, defillama_pool_uuid)
        metadata = get_metadata_by_project_symbol(project_symbol)
        tokens_metadata = _get_token_metadata(farm)
        result = place_value_into_categorized_portfolio_dict(
            categories,
            net_usd_value,
            length_of_categories,
            project,
            symbol,
            addr,
            apr,
            metadata,
            tokens_metadata,
            result,
        )
    return result


def _calculate_net_usd_valud(farm: dict) -> float:
    usd_value = 0
    for token in farm["tokens"]:
        usd_value += token["price"] * token["balance"]
    return usd_value


def _get_correct_addr(farm_obj: dict, address_column: str) -> str:
    for token in farm_obj[address_column]:
        if token["address"].startswith("ibc"):
            return token["address"].split("ibc/")[1] + ":osmosis"
    raise NotImplementedError(
        "Nansen handler doesn't support non-ibc address yet, for nansen's COSMOS data, you need to manually replace uatom to ibc/DEC41A02E47658D40FC71E5A35A9C807111F5A6662A3FB5DA84C4E6F53E616B3. It's a fake cosmos stake address"
    )


def _get_token_metadata(farm_obj: dict) -> list:
    return [
        {
            k: v
            for k, v in token.items()
            if k in {"address", "symbol", "chain", "name", "price", "balance"}
        }
        for token in farm_obj["tokens"]
    ]
