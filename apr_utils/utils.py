from portfolio_config import ADDRESS_2_CATEGORY

def get_metadata_by_symbol(symbol: str) -> dict:
    for metadata in ADDRESS_2_CATEGORY.values():
        if metadata['symbol'].lower() == symbol.lower():
            return metadata
    raise Exception(f"Cannot find {symbol} in your address mapping table")


def convert_apy_to_apr(apy: float) -> float:
    return ((apy+1)**(1/365)-1)*365