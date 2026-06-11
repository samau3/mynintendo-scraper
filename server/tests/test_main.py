import pytest

from main import is_incomplete_scrape


@pytest.mark.parametrize(
    "last_items,scraped_items,expansion_meta,expected",
    [
        (
            {},
            {"Item A": "100 Platinum Points"},
            {"expanded": False, "count_after": 1},
            False,
        ),
        (
            {"Item A": "100 Platinum Points", "Item B": "200 Platinum Points"},
            {"Item A": "100 Platinum Points", "Item B": "200 Platinum Points"},
            {"expanded": True, "count_after": 2},
            False,
        ),
        (
            {f"Item {i}": f"{i}00 Platinum Points" for i in range(59)},
            {f"Item {i}": f"{i}00 Platinum Points" for i in range(20)},
            {"expanded": False, "count_before": 20, "count_after": 20},
            True,
        ),
        (
            {"Item A": "100 Platinum Points", "Item B": "200 Platinum Points"},
            {"Item A": "100 Platinum Points", "Item C": "300 Platinum Points"},
            {"expanded": False, "count_after": 2},
            False,
        ),
        (
            {f"Item {i}": f"{i}00 Platinum Points" for i in range(59)},
            {f"Item {i}": f"{i}00 Platinum Points" for i in range(20)},
            {"expanded": True, "count_before": 20, "count_after": 20},
            True,
        ),
    ],
)
def test_is_incomplete_scrape(last_items, scraped_items, expansion_meta, expected):
    assert is_incomplete_scrape(last_items, scraped_items, expansion_meta) is expected
