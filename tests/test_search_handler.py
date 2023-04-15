"""
test Search Base's basic functions
"""
from search_handlers import SearchBase


def test_denormalize_tag() -> None:
    assert SearchBase.denormalize_tag(
        {"kepl", "eth"}, {"kepl", "eth"}.union({"strxeth"})
    ).intersection(
        SearchBase.denormalize_tag({"strxeth"}, {"kepl", "eth"}.union({"strxeth"}))
    ) == {
        "eth"
    }
    assert SearchBase.denormalize_tag(
        {"kepl", "eth"}, {"kepl", "eth"}.union({"strxeth"})
    ).union(
        SearchBase.denormalize_tag({"strxeth"}, {"kepl", "eth"}.union({"strxeth"}))
    ) == {
        "kepl",
        "eth",
    }
