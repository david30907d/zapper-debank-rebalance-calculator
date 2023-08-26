def convert_apy_to_apr(apy: float) -> float:
    # turn APY back to APR
    return ((apy + 1) ** (1 / 365) - 1) * 365


def convert_apr_to_apy(apr: float) -> float:
    """
    Convert APR to APY.

    :param apr: Annual Percentage Rate (as a percentage)
    :param compounds_per_year: Number of times the interest is compounded per year (default is 12 for monthly)
    :return: Annual Percentage Yield (as a percentage)
    """
    rate_per_compound = apr / 365
    return ((1 + rate_per_compound) ** 365 - 1) * 100
