from handlers.debank_handler import debank_handler
from handlers.nansen_handler import nansen_handler
from handlers.zapper_handler import zapper_handler


def get_data_source_handler(defi_portfolio_service_name) -> callable:
    if defi_portfolio_service_name == "zapper":
        return zapper_handler
    elif defi_portfolio_service_name == "debank":
        return debank_handler
    elif defi_portfolio_service_name == "nansen":
        return nansen_handler
    raise NotImplementedError(
        f"{defi_portfolio_service_name} handler not implemented yet"
    )
