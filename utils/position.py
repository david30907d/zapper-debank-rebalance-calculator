from rebalance_server.portfolio_config import (
    ADDRESS_2_CATEGORY,
    MIN_REBALANCE_POSITION_THRESHOLD,
)


def skip_rebalance_if_position_too_small(balanceUSD: float):
    return balanceUSD < MIN_REBALANCE_POSITION_THRESHOLD


def unwrap_token(symbol: str) -> str:
    if symbol.startswith("w"):
        return symbol[1:]
    return symbol


def get_metadata_by_project_symbol(project_symbol: str) -> dict:
    for address_and_project, metadata in ADDRESS_2_CATEGORY.items():
        project = address_and_project.split(":")[-1]
        if f'{project}:{metadata["symbol"]}'.lower() == project_symbol.lower():
            return metadata
    raise Exception(f"Cannot find {project_symbol} in your address mapping table")
