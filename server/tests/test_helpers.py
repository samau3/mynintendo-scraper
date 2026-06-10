from datetime import datetime, timedelta
from unittest.mock import Mock

import pytest
from bs4 import BeautifulSoup

from errors import CSSTagSelectorError
from helpers.calculate_expiration_date import (
    DateTimeProvider,
    calculate_expiration_date,
)
from helpers.find_items import find_items
from helpers.index_of_common_strings import index_of_common_strings
from helpers.remove_trademark_false_positives import remove_trademark_false_positives
from helpers.remove_trademark_symbols import remove_trademark_symbols
from main import get_items

MOCK_HTML = """
<html>
    <body>
        <a aria-label="Item 1 (Normal)" class="sc-1bsju6x-1">
            <div class="Hc9FH pRPVc EKAzI">Exclusive</div>
            <div data-testid="platinumPoints" class="Zc8hG">
                <img class="EgihB" src="IMAGE_URL">
                <span class="pXrQP">800</span> Platinum Points
            </div>
        </a>
        <a aria-label="Item 2 (Sold Out)" class="sc-1bsju6x-1">
            <div class="Hc9FH Qvcxb EKAzI">Sold Out</div>
            <div data-testid="platinumPoints" class="Zc8hG">
                <img class="EgihB" src="IMAGE_URL">
                <span class="unbAu">800</span> Platinum Points
            </div>
        </a>
    </body>
</html>
"""


def test_calculate_expiration_date():
    fixed_datetime = datetime(2023, 8, 20, 12, 0, 0)
    datetime_provider = Mock(spec=DateTimeProvider)
    datetime_provider.get_utc_now.return_value = fixed_datetime

    result = calculate_expiration_date(7, datetime_provider)
    assert result == fixed_datetime + timedelta(days=7)


@pytest.mark.parametrize(
    "list1,list2,expected",
    [
        (["apple", "banana", "orange"], ["kiwi", "banana", "orange"], ([1, 2], [1, 2])),
        (["apple", "banana", "orange"], ["kiwi", "grape", "pear"], ([], [])),
        ([], [], ([], [])),
        (["apple", "banana", "orange"], ["kiwi", "banana", "apple"], ([0, 1], [2, 1])),
    ],
)
def test_index_of_common_strings(list1, list2, expected):
    assert index_of_common_strings(list1, list2) == expected


@pytest.mark.parametrize(
    "input_list,expected",
    [
        (["Apple™", "Banana", "Orange™"], ["Apple", "Banana", "Orange"]),
        ([], []),
        (["Apple", "Banana", "Orange"], ["Apple", "Banana", "Orange"]),
    ],
)
def test_remove_trademark_symbols(input_list, expected):
    assert remove_trademark_symbols(input_list) == expected


def test_remove_trademark_false_positives():
    differences = {
        "dictionary_item_added": ["Apple™", "Banana", "Orange™"],
        "dictionary_item_removed": ["Apple", "Banana™", "Kiwi"],
    }
    result = remove_trademark_false_positives(differences)
    assert result == {
        "dictionary_item_added": ["Orange™"],
        "dictionary_item_removed": ["Kiwi"],
    }


def test_remove_trademark_false_positives_values_changed():
    differences = {"values_changed": {"root[2]": {"new_value": 4, "old_value": 2}}}
    assert remove_trademark_false_positives(differences) == differences


def test_find_items_css_error():
    with pytest.raises(CSSTagSelectorError, match="Reward product items not found"):
        find_items(BeautifulSoup("<html></html>", "lxml"))


def test_get_items_parses_mock_html():
    items = find_items(BeautifulSoup(MOCK_HTML, "lxml"))
    item_costs = get_items(items)
    item_costs["Item 1 (Normal)"] = item_costs["Item 1 (Normal)"].strip()
    assert item_costs == {
        "Item 1 (Normal)": "800 Platinum Points",
        "Item 2 (Sold Out)": "Sold Out",
    }


def test_get_items_css_stock_error():
    bad_html = MOCK_HTML.replace("Hc9FH", "CHANGED_TAG")
    items = find_items(BeautifulSoup(bad_html, "lxml"))
    with pytest.raises(CSSTagSelectorError, match="CSS tag for stock"):
        get_items(items)
