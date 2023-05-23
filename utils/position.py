from rebalance_server.portfolio_config import MIN_REBALANCE_POSITION_THRESHOLD


def skip_rebalance_if_position_too_small(balanceUSD: float):
    return balanceUSD < MIN_REBALANCE_POSITION_THRESHOLD


def unwrap_token(symbol: str) -> str:
    if symbol.startswith("w"):
        return symbol[1:]
    return symbol
