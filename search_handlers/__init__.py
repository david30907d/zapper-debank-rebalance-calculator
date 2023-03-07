from abc import ABC


class SearchBase(ABC):
    def __init__(self, *args, **kwargs):
        pass

    def check_similarity(self, symbol: str):
        raise NotImplementedError

    def unwrap_token(self, symbol: str) -> str:
        if symbol.startswith("w"):
            return symbol[1:]
        return symbol
