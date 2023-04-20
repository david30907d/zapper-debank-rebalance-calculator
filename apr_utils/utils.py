from portfolio_config import ADDRESS_2_CATEGORY


def get_metadata_by_project_symbol(project_symbol: str) -> dict:
    for metadata in ADDRESS_2_CATEGORY.values():
        if (
            f'{metadata["project"]}:{metadata["symbol"]}'.lower()
            == project_symbol.lower()
        ):
            return metadata
    raise Exception(f"Cannot find {project_symbol} in your address mapping table")


def convert_apy_to_apr(apy: float) -> float:
    # turn APY back to APR
    return ((apy + 1) ** (1 / 365) - 1) * 365
