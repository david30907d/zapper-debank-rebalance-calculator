from apr_utils.apr_calculator import get_lowest_or_default_apr
from apr_utils.utils import get_metadata_by_symbol
from handlers.utils import place_value_into_categorized_portfolio_dict
from portfolio_config import ADDRESS_2_CATEGORY, MIN_REBALANCE_POSITION_THRESHOLD


def _nansen_handler(positions, result):
    if "farms" in positions:
        return _nansen_farm_handler(positions, result)
    elif "delegation" in positions:
        return _nansen_stake_handler(positions, result)


def _nansen_farm_handler(positions, result):
    for farm in positions["farms"]:
        addr = _get_correct_addr(farm, address_column="tokens")
        net_usd_valud = _calculate_net_usd_valud(farm)
        # sanity check
        if net_usd_valud < MIN_REBALANCE_POSITION_THRESHOLD:
            continue
        categories = ADDRESS_2_CATEGORY[addr]["categories"]
        symbol = ADDRESS_2_CATEGORY[addr]["symbol"].lower()

        length_of_categories = len(categories)
        apr = get_lowest_or_default_apr(symbol)
        metadata = get_metadata_by_symbol(symbol)
        tokens_metadata = _get_token_metadata(farm)
        result = place_value_into_categorized_portfolio_dict(
            categories,
            net_usd_valud,
            length_of_categories,
            symbol,
            apr,
            metadata,
            tokens_metadata,
            result,
        )
    return result


def _nansen_stake_handler(positions, result):
    for farm in positions["delegation"]:
        addr = _get_correct_addr(farm, address_column="rewards")
        net_usd_valud = _calculate_net_usd_valud(farm)
        categories = ADDRESS_2_CATEGORY[addr]["categories"]
        symbol = ADDRESS_2_CATEGORY[addr]["symbol"].lower()

        length_of_categories = len(categories)
        apr = get_lowest_or_default_apr(symbol)
        metadata = get_metadata_by_symbol(symbol)
        tokens_metadata = _get_token_metadata(farm)
        result = place_value_into_categorized_portfolio_dict(
            categories,
            net_usd_valud,
            length_of_categories,
            symbol,
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
            return token["address"].split("ibc/")[1]
    raise NotImplementedError("Nansen handler doesn't support non-ibc address yet")


def _get_token_metadata(farm_obj: dict) -> list:
    return [
        {
            k: v
            for k, v in token.items()
            if k in {"address", "symbol", "chain", "name", "price", "balance"}
        }
        for token in farm_obj["tokens"]
    ]
