from unittest import TestCase, main
from unittest.mock import patch, Mock
from main import check_items


class TestCheckItemsFunction(TestCase):

    @patch('main.requests.get')  # Mocking the requests.get function
    def test_check_items_in_stock(self, mock_get):
        # Mocked HTML content for testing
        mock_html_text = """
            <div class="BasicTilestyles__Info-sc">
                <div>
                    <h2>Item 1</h2>
                </div>
                <div class="ProductTilestyles__DescriptionTag-sc">Exclusive</div>
                <div class="ProductTilestyles__PriceWrapper-sc">
                    <div>
                        <div>
                            <span>
                                <div>
                                    <span>$10</span>
                                </div>
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        """

        # Create a mock response object and configure its behavior
        mock_response = Mock()
        mock_response.text = mock_html_text
        mock_get.return_value = mock_response

        expected_result = {
            "Item 1": "$10"
        }

        result = check_items()
        self.assertEqual(result, expected_result)


    @patch('main.requests.get')  # Mocking the requests.get function
    def test_check_items_no_stock(self, mock_get):
        # Mocked HTML content for testing
        mock_html_text = """
            <div class="BasicTilestyles__Info-sc">
                <div>
                    <h2>Item 1</h2>
                </div>
                <div class="ProductTilestyles__DescriptionTag-sc">Out of Stock</div>
                <div class="ProductTilestyles__PriceWrapper-sc">
                    <div>
                        <div>
                            <span>
                                <div>
                                    <span>$10</span>
                                </div>
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        """

        # Create a mock response object and configure its behavior
        mock_response = Mock()
        mock_response.text = mock_html_text
        mock_get.return_value = mock_response

        expected_result = {
            "Item 1": "Out of Stock"
        }

        result = check_items()
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    main()
