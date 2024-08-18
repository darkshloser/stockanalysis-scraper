import unittest
from unittest.mock import patch, MagicMock
from selenium.webdriver.common.by import By
from stockanalysis_scraper.scraper.scraper import StockAnalysis
from stockanalysis_scraper.scraper.enums import MarketMovers, PremarketOptions

class TestStockAnalysis(unittest.TestCase):

    @patch('stockanalysis_scraper.scraper.scraper.webdriver.Chrome')
    @patch('stockanalysis_scraper.scraper.scraper.ChromeDriverManager')
    @patch('stockanalysis_scraper.scraper.scraper.get_settings')
    def setUp(self, mock_get_settings, mock_chromedriver_manager, mock_chrome):
        # Mocking the Chrome WebDriver and its methods
        self.mock_driver = MagicMock()
        mock_chrome.return_value = self.mock_driver
        mock_chromedriver_manager().install.return_value = '/path/to/chromedriver'
        
        # Mock the base URL setting
        mock_get_settings.return_value = {'base_url': 'https://stockanalysis.com/'}
        
        self.stock_analysis = StockAnalysis()
        self.base_url = 'https://stockanalysis.com/'

    def test_set_url_premarket_gainers(self):
        self.stock_analysis.set_url(self.base_url, MarketMovers.PREMARKET, PremarketOptions.GAINERS)
        expected_url = 'https://stockanalysis.com/markets/premarket/gainers/'
        self.assertEqual(self.stock_analysis.url, expected_url)

    @patch('stockanalysis_scraper.scraper.scraper.BeautifulSoup')
    def test_parse_page_content(self, mock_beautifulsoup):
        mock_html = '<html></html>'
        self.mock_driver.page_source = mock_html
        self.stock_analysis.parse_page_content()
        mock_beautifulsoup.assert_called_with(mock_html, 'html.parser')

    @patch('stockanalysis_scraper.scraper.scraper.WebDriverWait')
    @patch('stockanalysis_scraper.scraper.scraper.EC')
    def test_click_button(self, mock_ec, mock_webdriver_wait):
        mock_element = MagicMock()
        mock_webdriver_wait.return_value.until.return_value = mock_element

        self.stock_analysis.click_button(By.CLASS_NAME, 'controls-btn')
        mock_webdriver_wait.return_value.until.assert_called_with(mock_ec.element_to_be_clickable((By.CLASS_NAME, 'controls-btn')))
        mock_element.click.assert_called_once()

    @patch('stockanalysis_scraper.scraper.scraper.time.sleep')
    def test_extract_table_rows(self, mock_sleep):
        self.mock_driver.find_element.return_value = MagicMock()
        mock_soup = MagicMock()
        self.stock_analysis.parse_page_content = MagicMock(return_value=mock_soup)
        mock_tbody = MagicMock()
        mock_soup.find.return_value = mock_tbody
        mock_row = MagicMock()
        mock_tbody.find_all.return_value = [mock_row]
        mock_td = MagicMock()
        mock_row.find_all.return_value = [mock_td]
        mock_td.text.strip.return_value = 'test_data'
        
        result = self.stock_analysis._extract_table_rows()
        self.assertEqual(result, [['test_data']])

    def test_scrape_premarket_gainers(self):
        self.stock_analysis.set_url = MagicMock()
        self.stock_analysis.open_url = MagicMock()
        self.stock_analysis._extract_table_rows = MagicMock(return_value=[['test_data']])
        self.stock_analysis.close = MagicMock()

        result = self.stock_analysis.scrape_premarket_gainers(self.base_url)
        self.assertEqual(result, [['test_data']])

    def test_not_implemented_methods(self):
        with self.assertRaises(NotImplementedError):
            self.stock_analysis.scrape_premarket_movers(self.base_url)
        with self.assertRaises(NotImplementedError):
            self.stock_analysis.scrape_premarket_losers(self.base_url)

if __name__ == '__main__':
    unittest.main()