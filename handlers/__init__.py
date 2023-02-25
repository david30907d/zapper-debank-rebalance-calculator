from handlers.debank_handler import _debank_handler
from handlers.zapper_handler import _zapper_handler
def get_data_source_handler(defi_portfolio_service_name) -> callable:
    if defi_portfolio_service_name == "zapper":
        return _zapper_handler
    elif defi_portfolio_service_name == "debank":
        return _debank_handler
    raise NotImplementedError
