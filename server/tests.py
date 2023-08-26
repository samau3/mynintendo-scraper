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

    @patch('requests.get')
    def test_check_items(self, mock_get):

        mock_html_text = """
            <div class="BasicTilestyles__Info-sc">
                <div>
                    <h2>Item 1</h2>
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
                                        <span>$10</span>
                                    </span>
                                </div>
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        """


        mock_response = Mock()
        mock_response.text = mock_html_text
        mock_get.return_value = mock_response

        item_costs = check_items()
        item_costs["Item 1"] = item_costs["Item 1"].strip()

        self.assertEqual(item_costs, {'Item 1': '$10'})

        
    @patch('requests.get')    
    def test_check_items_no_stock(self, mock_get):
        # Mocked HTML content for testing
        mock_html_text = """
            <div class="BasicTilestyles__Info-sc">
                <div>
                    <h2>Item 1</h2>
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
                                        <span>$10</span>
                                    </span>
                                </div>
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        """

        mock_response = Mock()
        mock_response.text = mock_html_text
        mock_get.return_value = mock_response

        expected_result = {
            "Item 1": "Sold out"
        }

        result = check_items()
        self.assertEqual(result, expected_result)

    @patch('requests.get')
    def test_check_items_css_error(self, mock_get):
        mock_response = Mock()
        mock_response.text = "<html></html>"
        mock_get.return_value = mock_response

        with self.assertRaises(CSSTagSelectorError):
            check_items()


if __name__ == '__main__':
    main()
