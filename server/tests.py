from unittest import TestCase, main
from unittest.mock import patch, Mock
from datetime import datetime, timedelta

from main import check_items
from errors import CSSTagSelectorError
from helpers.calculate_expiration_date import calculate_expiration_date, DateTimeProvider


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
        

        self.assertEqual(item_costs, {'Item 1 (Sold out)': 'Sold out', 'Item 2 (Normal)': '$15', 'Item 3 (CSS price tag changed)': 'Price Not Found'})

    @patch('requests.get')
    def test_check_items_css_error(self, mock_get):
        self.mock_response.text = "<html></html>"  # Simulate no items found
        mock_get.return_value = self.mock_response

        with self.assertRaises(CSSTagSelectorError):
            check_items()


if __name__ == '__main__':
    main()
