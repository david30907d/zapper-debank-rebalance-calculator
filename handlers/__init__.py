from rebalance_server.handlers.debank_handler import debank_handler
from rebalance_server.handlers.nansen_handler import nansen_handler


def get_data_source_handler(defi_portfolio_service_name) -> callable:
    if defi_portfolio_service_name == "debank":
        return debank_handler
    elif defi_portfolio_service_name == "nansen":
        return nansen_handler
    raise NotImplementedError(
        f"{defi_portfolio_service_name} handler not implemented yet"
    )
