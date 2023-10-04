def place_value_into_categorized_portfolio_dict(
    categories: list,
    net_usd_valud: float,
    length_of_categories: int,
    project: str,
    symbol: str,
    unique_id: str,
    apr: float,
    metadata: dict,
    tokens_metadata: list,
    protocol_logo_url: str,
    result: dict,
):
    for category in categories:
        weighted_balanceUSD = get_weighted_balanceUSD(
            net_usd_valud, category, metadata, length_of_categories
        )
        result[category]["portfolio"][f"{project}:{symbol}"][
            "worth"
        ] += weighted_balanceUSD
        result[category]["portfolio"][f"{project}:{symbol}"]["address"] = unique_id
        result[category]["portfolio"][f"{project}:{symbol}"]["APR"] = apr
        result[category]["portfolio"][f"{project}:{symbol}"][
            "protocol_logo_url"
        ] = protocol_logo_url
        result[category]["portfolio"][f"{project}:{symbol}"]["metadata"] = metadata
        result[category]["portfolio"][f"{project}:{symbol}"][
            "tokens_metadata"
        ] = tokens_metadata
        result[category]["sum"] += weighted_balanceUSD
    return result


def get_weighted_balanceUSD(
    net_usd_valud: float, category: str, metadata: dict, length_of_categories: int
):
    if length_of_categories == 1:
        return net_usd_valud
    elif "eth" in metadata["composition"]:
        if category == "long_term_bond":
            return net_usd_valud * metadata["composition"]["eth"]
        else:
            return (
                net_usd_valud
                * (1 - metadata["composition"]["eth"])
                / (length_of_categories - 1)
            )
    return net_usd_valud / length_of_categories
