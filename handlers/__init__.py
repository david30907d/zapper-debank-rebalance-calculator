from handlers.debank_handler import _debank_handler
from handlers.nansen_handler import _nansen_handler
from handlers.zapper_handler import _zapper_handler


def get_data_source_handler(defi_portfolio_service_name) -> callable:
    if defi_portfolio_service_name == "zapper":
        return _zapper_handler
    elif defi_portfolio_service_name == "debank":
        return _debank_handler
    elif defi_portfolio_service_name == "nansen":
        return _nansen_handler
    raise NotImplementedError(
        f"{defi_portfolio_service_name} handler not implemented yet"
    )
