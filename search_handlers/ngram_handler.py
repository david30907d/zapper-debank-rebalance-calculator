import ngram

from search_handlers import SearchBase


class NgramSimilarityHandler(SearchBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.similarity_threshold = kwargs["similarity_threshold"]

    def check_similarity(self, metadata: dict, candidate_symbol: str) -> float:
        return (
            ngram.NGram.compare(
                self.unwrap_token(metadata["metadata"]["symbol"].lower()),
                self.unwrap_token(candidate_symbol.lower()),
            )
            > self.similarity_threshold
        )
