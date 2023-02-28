from collections import defaultdict


def get_networh_to_balance_adapter(adapter: str) -> callable:
    if adapter == "coingecko":
        return coingecko_net_worth_2_balance_adapter
    raise NotImplementedError(f"adapter {adapter} not implemented")


def coingecko_net_worth_2_balance_adapter(categorized_positions: dict) -> float:
    dedupe_symbol_set = set()
    result = defaultdict(list)
    for category_obj in categorized_positions.values():
        for symbol, position_obj in category_obj["portfolio"].items():
            if symbol in dedupe_symbol_set:
                continue
            dedupe_symbol_set.add(symbol)
            for tokens in position_obj["tokens_metadata"]:
                token_array = []
                if "tokens" not in tokens:
                    result[symbol].append(tokens)
                else:
                    _get_basic_token_in_backtracking_way(token_array, tokens["tokens"])
                    result[symbol] += token_array
    return result


def _get_basic_token_in_backtracking_way(
    token_array, token_array_consistes_of_token_dict: list
):
    for token in token_array_consistes_of_token_dict:
        if "tokens" not in token:
            token_array.append(token)
            continue
        _get_basic_token_in_backtracking_way(token_array, token["tokens"])
