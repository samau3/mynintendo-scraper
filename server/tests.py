from unittest import TestCase, main
from unittest.mock import patch, Mock
from datetime import datetime, timedelta

from main import check_items
from errors import CSSTagSelectorError
from helpers.calculate_expiration_date import calculate_expiration_date, DateTimeProvider
from helpers.remove_trademark_false_positives import remove_trademark_false_positives
from helpers.index_of_common_strings import index_of_common_strings
from helpers.remove_trademark_symbols import remove_trademark_symbols


class TestCalculateExpDate(TestCase):
    def test_calculate_expiration_date(self):
        number_of_days = 7
        # Choose a fixed datetime for testing
        fixed_datetime = datetime(2023, 8, 20, 12, 0, 0)

        # Mock DateTimeProvider to return the fixed_datetime
        datetime_provider = Mock(spec=DateTimeProvider)
        datetime_provider.get_utc_now.return_value = fixed_datetime

        expected_result = fixed_datetime + timedelta(days=number_of_days)

        result = calculate_expiration_date(number_of_days, datetime_provider)
        self.assertEqual(result, expected_result)


class TestIndexOfCommonStrings(TestCase):
    def test_index_of_common_strings(self):
        list1 = ['apple', 'banana', 'orange']
        list2 = ['kiwi', 'banana', 'orange']
        result = index_of_common_strings(list1, list2)
        self.assertEqual(result, ([1, 2], [1, 2]))

    def test_index_of_common_strings_no_common_strings(self):
        list1 = ['apple', 'banana', 'orange']
        list2 = ['kiwi', 'grape', 'pear']
        result = index_of_common_strings(list1, list2)
        self.assertEqual(result, ([], []))

    def test_index_of_common_strings_empty_lists(self):
        list1 = []
        list2 = []
        result = index_of_common_strings(list1, list2)
        self.assertEqual(result, ([], []))

    def test_index_of_common_strings_one_empty_list(self):
        list1 = ['apple', 'banana', 'orange']
        list2 = ['kiwi', 'banana', 'apple']
        result = index_of_common_strings(list1, list2)
        self.assertEqual(result, ([0, 1], [2, 1]))


class TestRemoveTrademarkSymbols(TestCase):
    def test_remove_trademark_symbols(self):
        input_list = ["Apple™", "Banana", "Orange™"]
        result = remove_trademark_symbols(input_list)
        self.assertEqual(result, ['Apple', 'Banana', 'Orange'])

    def test_remove_trademark_symbols_empty_list(self):
        input_list = []
        result = remove_trademark_symbols(input_list)
        self.assertEqual(result, [])

    def test_remove_trademark_symbols_no_trademark_symbols(self):
        input_list = ["Apple", "Banana", "Orange"]
        result = remove_trademark_symbols(input_list)
        self.assertEqual(result, ['Apple', 'Banana', 'Orange'])


class TestRemoveTrademarkFalsePositives(TestCase):
    def test_remove_trademark_false_positives(self):
        differences = {
            "dictionary_item_added": ["Apple™", "Banana", "Orange™"],
            "dictionary_item_removed": ["Apple", "Banana™", "Kiwi"]
        }
        result = remove_trademark_false_positives(differences)
        self.assertEqual(result, {'dictionary_item_added': [
                         'Orange™'], 'dictionary_item_removed': ['Kiwi']})

    def test_remove_trademark_false_positives_out_of_order(self):
        differences = {
            "dictionary_item_added": ["Apple™", "Banana", "Orange™", "Kiwi™"],
            "dictionary_item_removed": ["Apple", "Banana™", "Kiwi"]
        }
        result = remove_trademark_false_positives(differences)
        self.assertEqual(result, {'dictionary_item_added': [
                         'Orange™']})

    def test_remove_trademark_false_positives_no_common_strings(self):
        differences = {
            "dictionary_item_added": ["Apple™", "Banana", "Orange™"],
            "dictionary_item_removed": ["Kiwi", "Grape", "Pear"]
        }
        result = remove_trademark_false_positives(differences)
        self.assertEqual(result, differences)

    def test_remove_trademark_false_positives_empty_lists(self):
        differences = {
            "dictionary_item_added": [],
            "dictionary_item_removed": []
        }
        result = remove_trademark_false_positives(differences)
        self.assertEqual(result, differences)


class TestCheckItemsFunction(TestCase):

    def setUp(self):
        self.mock_response = Mock()
        self.mock_response.text = """
            <html>
                <body>
                    <div class="sc-1bsju6x-4 eJevZe">
                        <div class="sc-1bsju6x-6 irzLJU">
                            <div class="sc-eg7slj-1 ieWZCg" style="color: rgb(72, 72, 72);">
                                <h2 class="sc-s17bth-0 bMmuUN sc-w55g5t-0 gSthvS sc-eg7slj-2 iiGOlC">Item 1 (Normal)</h2>
                                <div class="sc-m1loqs-5 bvcBeK"></div>
                            </div>
                            <div class="sc-tb903t-0 hwFxtm sc-m1loqs-4 gXVfCV">Exclusive</div>
                            <div class="sc-m1loqs-3 gGJMHZ">
                                <div class="sc-1f0n8u6-0 kNfSFq">
                                    <div class="sc-1f0n8u6-1 icpwvf">
                                        <span class="sc-1f0n8u6-5 fpvyxr">
                                            <span class="sc-1gv8hi6-0 lktkyu sc-1f0n8u6-2 bFvx">Regular Price:</span>
                                            <div data-testid="platinumPoints" class="sc-1f0n8u6-8 ftpArF">
                                                <div class="sc-1244ond-0 bYKqUR sc-1yh2edi-0 GtTvR sc-1f0n8u6-7 gcszdM">
                                                    <img alt="" loading="lazy" fetchpriority="low" class="sc-1244ond-1 eaPLXy" src="IMAGE_URL">
                                                </div>
                                                <span class="sc-1f0n8u6-10 imlIYl">
                                                    <span class="sc-1f0n8u6-9 unbAu">800</span> Platinum Points
                                                </span>
                                            </div>
                                        </span>
                                    </div>
                                </div>
                            </div>
                            <div class="sc-eg7slj-0 cstaaz">
                                <div class="sc-v8r1lj-1 UbrcP">
                                    <div class="sc-v8r1lj-0 dQBnrT"></div>
                                    <span>Exclusives</span>
                                </div>
                                <button class="sc-1ud0cp0-0 jhpscK sc-m1loqs-0 jgyRXQ" title="Add to Wish List" aria-label="Add to Wish List" aria-pressed="false">
                                    <svg viewBox="0 0 54 54" fill="currentColor" stroke="currentColor" width="24" role="presentation" alt="" data-testid="heartspark" color="currentColor" size="24">
                                        <g class="hearts">
                                            <path ></path>
                                            <path ></path>
                                        </g>
                                        <g class="sparks">
                                            <path ></path>
                                            <path ></path>
                                        <path ></path>
                                        <path ></path>
                                        </g>
                                    </svg>
                                </button>
                            </div>
                        </div>
                    </div>
                    <div class="sc-1bsju6x-4 eJevZe">
                        <div class="sc-1bsju6x-6 irzLJU">
                            <div class="sc-eg7slj-1 ieWZCg" style="color: rgb(72, 72, 72);">
                                <h2 class="sc-s17bth-0 bMmuUN sc-w55g5t-0 gSthvS sc-eg7slj-2 iiGOlC">Item 2 (Sold Out)</h2>
                                <div class="sc-m1loqs-5 bvcBeK"></div>
                            </div>
                            <div class="sc-tb903t-0 hwFxtm sc-m1loqs-4 gXVfCV">Sold Out</div>
                            <div class="sc-m1loqs-3 gGJMHZ">
                                <div class="sc-1f0n8u6-0 kNfSFq">
                                    <div class="sc-1f0n8u6-1 icpwvf">
                                        <span class="sc-1f0n8u6-5 fpvyxr">
                                            <span class="sc-1gv8hi6-0 lktkyu sc-1f0n8u6-2 bFvx">Regular Price:</span>
                                            <div data-testid="platinumPoints" class="sc-1f0n8u6-8 ftpArF">
                                                <div class="sc-1244ond-0 bYKqUR sc-1yh2edi-0 GtTvR sc-1f0n8u6-7 gcszdM">
                                                    <img alt="" loading="lazy" fetchpriority="low" class="sc-1244ond-1 eaPLXy" src="IMAGE_URL">
                                                </div>
                                                <span class="sc-1f0n8u6-10 imlIYl">
                                                    <span class="sc-1f0n8u6-9 unbAu">800</span>
                                                    <!-- -->Platinum Points
                                                </span>
                                            </div>
                                        </span>
                                    </div>
                                </div>
                            </div>
                            <div class="sc-eg7slj-0 cstaaz">
                                <div class="sc-v8r1lj-1 UbrcP">
                                    <div class="sc-v8r1lj-0 dQBnrT"></div>
                                    <span>Exclusives</span>
                                </div>
                                <button class="sc-1ud0cp0-0 jhpscK sc-m1loqs-0 jgyRXQ" title="Add to Wish List" aria-label="Add to Wish List" aria-pressed="false">
                                    <svg viewBox="0 0 54 54" fill="currentColor" stroke="currentColor" width="24" role="presentation" alt="" data-testid="heartspark" color="currentColor" size="24">
                                        <g class="hearts">
                                            <path ></path>
                                            <path ></path>
                                        </g>
                                        <g class="sparks">
                                            <path ></path>
                                            <path ></path>
                                        <path ></path>
                                        <path ></path>
                                        </g>
                                    </svg>
                                </button>
                            </div>
                        </div>
                    </div>
                </body>
            </html>
        """

    @patch('requests.get')
    def test_check_items(self, mock_get):
        mock_get.return_value = self.mock_response

        item_costs = check_items()
        item_costs['Item 1 (Normal)'] = item_costs['Item 1 (Normal)'].strip()

        self.assertEqual(item_costs, {'Item 1 (Normal)': '800 Platinum Points',
                         'Item 2 (Sold Out)': 'Sold Out'})

    @patch('requests.get')
    def test_check_items_css_error(self, mock_get):
        self.mock_response.text = "<html></html>"  # Simulate no items found
        mock_get.return_value = self.mock_response

        with self.assertRaises(CSSTagSelectorError):
            check_items()

    @patch('requests.get')
    def test_check_items_css_price_error(self, mock_get):
        self.mock_response.text = """
            <html>
                <body>
                    <div class="sc-1bsju6x-4 eJevZe">
                        <div class="sc-1bsju6x-6 irzLJU">
                            <div class="sc-eg7slj-1 ieWZCg" style="color: rgb(72, 72, 72);">
                                <h2 class="sc-s17bth-0 bMmuUN sc-w55g5t-0 gSthvS sc-eg7slj-2 iiGOlC">Item 1 (Normal)</h2>
                                <div class="sc-m1loqs-5 bvcBeK"></div>
                            </div>
                            <div class="CHANGED_TAG">Exclusive</div>
                            <div class="sc-m1loqs-3 gGJMHZ">
                                <div class="sc-1f0n8u6-0 kNfSFq">
                                    <div class="sc-1f0n8u6-1 icpwvf">
                                        <span class="sc-1f0n8u6-5 fpvyxr">
                                            <span class="sc-1gv8hi6-0 lktkyu sc-1f0n8u6-2 bFvx">Regular Price:</span>
                                            <div data-testid="platinumPoints" class="sc-1f0n8u6-8 ftpArF">
                                                <div class="sc-1244ond-0 bYKqUR sc-1yh2edi-0 GtTvR sc-1f0n8u6-7 gcszdM">
                                                    <img alt="" loading="lazy" fetchpriority="low" class="sc-1244ond-1 eaPLXy" src="IMAGE_URL">
                                                </div>
                                                <span class="sc-1f0n8u6-10 imlIYl">
                                                    <span class="sc-1f0n8u6-9 unbAu">800</span> Platinum Points
                                                </span>
                                            </div>
                                        </span>
                                    </div>
                                </div>
                            </div>
                            <div class="sc-eg7slj-0 cstaaz">
                                <div class="sc-v8r1lj-1 UbrcP">
                                    <div class="sc-v8r1lj-0 dQBnrT"></div>
                                    <span>Exclusives</span>
                                </div>
                                <button class="sc-1ud0cp0-0 jhpscK sc-m1loqs-0 jgyRXQ" title="Add to Wish List" aria-label="Add to Wish List" aria-pressed="false">
                                    <svg viewBox="0 0 54 54" fill="currentColor" stroke="currentColor" width="24" role="presentation" alt="" data-testid="heartspark" color="currentColor" size="24">
                                        <g class="hearts">
                                            <path ></path>
                                            <path ></path>
                                        </g>
                                        <g class="sparks">
                                            <path ></path>
                                            <path ></path>
                                        <path ></path>
                                        <path ></path>
                                        </g>
                                    </svg>
                                </button>
                            </div>
                        </div>
                    </div>
                </body>
            </html>
        """
        mock_get.return_value = self.mock_response

        with self.assertRaises(CSSTagSelectorError):
            check_items()


if __name__ == '__main__':
    main()
