from rebalance_server.portfolio_config import MIN_REBALANCE_POSITION_THRESHOLD


def skip_rebalance_if_position_too_small(balanceUSD: float):
    return balanceUSD < MIN_REBALANCE_POSITION_THRESHOLD
