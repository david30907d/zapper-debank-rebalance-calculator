from search_handlers import SearchBase


class JaccardSimilarityHandler(SearchBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.similarity_threshold = kwargs["similarity_threshold"]

    def check_similarity(self, metadata: dict, candidate_symbol: str) -> float:
        my_pool_tags = set(
            self.unwrap_token(tag.lower()) for tag in metadata["metadata"]["tags"]
        )
        candidate_pool_tags = set(
            self.unwrap_token(tag) for tag in candidate_symbol.split("-")
        )
        return (
            len(my_pool_tags.intersection(candidate_pool_tags))
            / len(my_pool_tags.union(candidate_pool_tags))
            > self.similarity_threshold
        )
