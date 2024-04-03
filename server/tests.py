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
                    <div class="BasicTilestyles__Info-sc">
                        <div>
                            <h2>Item 1 (Sold out)</h2>
                        </div>
                        <div class="ProductTilestyles__DescriptionTag-sc">Sold out</div>
                        <div class="ProductTilestyles__PriceWrapper-sc">
                            <div class="Pricestyles__Price-sc">
                                <div class="Pricestyles__Price-sc">
                                    <span class="Pricestyles_MSRP">
                                        <span class="ScreenReaderOnlystyles">Regular Price:</span>
                                        <div class="Pricestyles_PlatinumPoints">
                                            <div class="Imagestyles_ImageWrapper">
                                                <img>
                                            </div>
                                            <span class="Pricestyles_PlatinumPointsText">
                                                <span>Now: $10</span>
                                            </span>
                                        </div>
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="BasicTilestyles__Info-sc">
                        <div>
                            <h2>Item 2 (Normal)</h2>
                        </div>
                        <div class="ProductTilestyles__DescriptionTag-sc">Exclusive</div>
                        <div class="ProductTilestyles__PriceWrapper-sc">
                            <div class="Pricestyles__Price-sc">
                                <div class="Pricestyles__Price-sc">
                                    <span class="Pricestyles_MSRP">
                                        <span class="ScreenReaderOnlystyles">Regular Price:</span>
                                        <div class="Pricestyles_PlatinumPoints">
                                            <div class="Imagestyles_ImageWrapper">
                                                <img>
                                            </div>
                                            <span class="Pricestyles_PlatinumPointsText">
                                                <span>$15</span>
                                            </span>
                                        </div>
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="BasicTilestyles__Info-sc">
                        <div>
                            <h2>Item 3 (CSS price tag changed)</h2>
                        </div>
                        <div class="ProductTilestyles__DescriptionTag-sc">Exclusive</div>
                        <div class="ProductTilestyles__PriceWrapper-change">
                            <div class="Pricestyles__Price-sc">
                                <div class="Pricestyles__Price-sc">
                                    <span class="Pricestyles_MSRP">
                                        <span class="ScreenReaderOnlystyles">Regular Price:</span>
                                        <div class="Pricestyles_PlatinumPoints">
                                            <div class="Imagestyles_ImageWrapper">
                                                <img>
                                            </div>
                                            <span class="Pricestyles_PlatinumPointsText">
                                                <span>$15</span>
                                            </span>
                                        </div>
                                    </span>
                                </div>
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
        item_costs['Item 2 (Normal)'] = item_costs['Item 2 (Normal)'].strip()

        self.assertEqual(item_costs, {'Item 1 (Sold out)': 'Sold out',
                         'Item 2 (Normal)': '$15', 'Item 3 (CSS price tag changed)': 'Price Not Found'})

    @patch('requests.get')
    def test_check_items_css_error(self, mock_get):
        self.mock_response.text = "<html></html>"  # Simulate no items found
        mock_get.return_value = self.mock_response

        with self.assertRaises(CSSTagSelectorError):
            check_items()


if __name__ == '__main__':
    main()
