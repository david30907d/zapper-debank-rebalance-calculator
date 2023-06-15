def convert_apy_to_apr(apy: float) -> float:
    # turn APY back to APR
    return ((apy + 1) ** (1 / 365) - 1) * 365
