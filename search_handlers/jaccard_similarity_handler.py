from rebalance_server.search_handlers import SearchBase


class JaccardSimilarityHandler(SearchBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._similarity_threshold = kwargs["similarity_threshold"]

    @property
    def similarity_threshold(self):
        return self._similarity_threshold

    def get_similarity(self, metadata: dict, candidate_symbol: str) -> float:
        """Jaccard similarity between two sets of tags"""
        my_pool_tags = set(
            self.unwrap_token(tag.lower()) for tag in metadata["metadata"]["tags"]
        )
        candidate_pool_tags = set(
            self.unwrap_token(tag) for tag in candidate_symbol.split("-")
        )
        normalized_my_pool_tags = self.denormalize_tag(
            my_pool_tags, my_pool_tags.union(candidate_pool_tags)
        )
        normalized_candidate_pool_tags = self.denormalize_tag(
            candidate_pool_tags, my_pool_tags.union(candidate_pool_tags)
        )
        return len(
            normalized_my_pool_tags.intersection(normalized_candidate_pool_tags)
        ) / len(normalized_my_pool_tags.union(normalized_candidate_pool_tags))
