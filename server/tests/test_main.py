import pytest

from main import (
    derive_preview_item_count,
    is_incomplete_scrape,
    resolve_preview_item_count,
)


@pytest.mark.parametrize(
    "expansion_meta,expected",
    [
        (
            {
                "button_found": True,
                "count_before": 20,
                "count_after": 59,
                "expanded": True,
            },
            20,
        ),
        (
            {
                "button_found": False,
                "count_before": 45,
                "count_after": 45,
                "expanded": True,
            },
            None,
        ),
        (
            {
                "button_found": True,
                "count_before": 20,
                "count_after": 20,
                "expanded": False,
            },
            None,
        ),
    ],
)
def test_derive_preview_item_count(expansion_meta, expected):
    assert derive_preview_item_count(expansion_meta) == expected


def test_resolve_preview_item_count_carries_forward_last_record(app):
    from models import Listings, db

    with app.app_context():
        last_record = Listings.add_record(
            {"Item A": "100 Platinum Points"},
            preview_item_count=20,
        )
        db.session.commit()

        assert (
            resolve_preview_item_count(
                {
                    "button_found": False,
                    "count_before": 45,
                    "count_after": 45,
                    "expanded": True,
                },
                last_record,
            )
            == 20
        )


@pytest.mark.parametrize(
    "last_items,scraped_items,expansion_meta,preview_item_count,expected",
    [
        (
            {},
            {"Item A": "100 Platinum Points"},
            {"expanded": False, "count_after": 1},
            None,
            False,
        ),
        (
            {"Item A": "100 Platinum Points", "Item B": "200 Platinum Points"},
            {"Item A": "100 Platinum Points", "Item B": "200 Platinum Points"},
            {"expanded": True, "count_after": 2, "button_found": False},
            None,
            False,
        ),
        (
            {f"Item {i}": f"{i}00 Platinum Points" for i in range(59)},
            {f"Item {i}": f"{i}00 Platinum Points" for i in range(20)},
            {
                "expanded": False,
                "button_found": True,
                "count_before": 20,
                "count_after": 20,
            },
            20,
            True,
        ),
        (
            {"Item A": "100 Platinum Points", "Item B": "200 Platinum Points"},
            {"Item A": "100 Platinum Points", "Item C": "300 Platinum Points"},
            {"expanded": False, "count_after": 2, "button_found": False},
            None,
            False,
        ),
        (
            {f"Item {i}": f"{i}00 Platinum Points" for i in range(59)},
            {f"Item {i}": f"{i}00 Platinum Points" for i in range(20)},
            {
                "expanded": True,
                "button_found": False,
                "count_before": 20,
                "count_after": 20,
            },
            20,
            True,
        ),
        (
            {f"Item {i}": f"{i}00 Platinum Points" for i in range(59)},
            {f"Item {i}": f"{i}00 Platinum Points" for i in range(45)},
            {
                "expanded": True,
                "button_found": False,
                "count_before": 45,
                "count_after": 45,
            },
            20,
            False,
        ),
        (
            {f"Item {i}": f"{i}00 Platinum Points" for i in range(59)},
            {f"Item {i}": f"{i}00 Platinum Points" for i in range(20)},
            {
                "expanded": True,
                "button_found": True,
                "count_before": 20,
                "count_after": 20,
            },
            20,
            True,
        ),
    ],
)
def test_is_incomplete_scrape(
    last_items, scraped_items, expansion_meta, preview_item_count, expected
):
    assert (
        is_incomplete_scrape(
            last_items, scraped_items, expansion_meta, preview_item_count
        )
        is expected
    )
