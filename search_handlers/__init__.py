from abc import ABC


class SearchBase(ABC):
    """
    This is the base class for all search handlers
    """

    def __init__(self, *args, **kwargs):
        pass

    def check_similarity(self, symbol: str):
        raise NotImplementedError

    def unwrap_token(self, symbol: str) -> str:
        if symbol.startswith("w"):
            return symbol[1:]
        return symbol

    @staticmethod
    def denormalize_tag(tags1: set[str], union_tags: set[str]) -> set[str]:
        """
        1. This function is used to denormalize the tags, for example, if we have a tag "sfrxeth", we want to denormalize it to "eth"
        2. Also, set a contraint for length of tag, if the length of tag is less than 3, we don't think it's a variation of another tag
        """
        result_tag_set = set()
        for tag_a in tags1:
            added = False
            for tag_b in union_tags:
                if tag_a != tag_b and tag_a.endswith(tag_b) and len(tag_b) >= 3:
                    result_tag_set.add(tag_b)
                    added = True
                    break
            if added:
                continue
            result_tag_set.add(tag_a)

        return result_tag_set


if __name__ == "__main__":
    print(
        SearchBase.denormalize_tag(
            {"kepl", "eth"}, {"kepl", "eth"}.union({"strxeth"})
        ).intersection(
            SearchBase.denormalize_tag({"strxeth"}, {"kepl", "eth"}.union({"strxeth"}))
        )
    )
    print(
        SearchBase.denormalize_tag(
            {"kepl", "eth"}, {"kepl", "eth"}.union({"strxeth"})
        ).union(
            SearchBase.denormalize_tag({"strxeth"}, {"kepl", "eth"}.union({"strxeth"}))
        )
    )
