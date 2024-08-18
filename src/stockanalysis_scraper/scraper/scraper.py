import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from .config import get_settings
from .enums import MarketMovers, PremarketOptions, AfterHoursOptions, ActiveOptions, \
LosersOptions, GainersOptions, News, Stocks
from .urls import page_options


settings = get_settings()
base_url = settings['base_url']


class StockAnalysis:

    def __init__(self, headless=True, sendbox=True):
        try:
            self.options = webdriver.ChromeOptions()
            if headless:
                self.options.add_argument('--headless')
            if sendbox:
                self.options.add_argument('--no-sandbox')
            self.options.add_argument('--disable-dev-shm-usage')
            self.driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=self.options)
        except:
            raise ValueError("Currently only 'Chrome' browser is supported")

    def set_url(self, base_url: str, page: MarketMovers, option=None):
        url = base_url + page.value
        if option and option in page_options.get(page, {}):
            url += page_options[page].get(option,'')
        self.url = url

    def set_stock_url(self, stock_symbol: str):
        """
        Set the URL to retrieve data for a specific stock based on its symbol.
        """
        self.url = f"{base_url}/stocks/{stock_symbol}"

    def open_url(self):
        self.driver.get(self.url)
        self.driver.implicitly_wait(10)  # Wait for JavaScript to render

    def parse_page_content(self):
        html = self.driver.page_source
        return BeautifulSoup(html, 'html.parser')

    def close(self):
        self.driver.quit()

    def click_button(self, by: By, value: str):
        try:
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((by, value))
            )
            button.click()
            time.sleep(3)
            return
        except:
            pass
        raise Exception('Can not click on specified button.')

    def get_elements(self, by: By, value: str):
        return self.driver.find_elements(by, value)

    def scrape_premarket_movers(self, base_url: str):
        raise NotImplementedError("This method needs to be implemented.")
    
    def _extract_table_rows(self):
        try:
            # Wait until the button container is visible
            self.click_button(By.CLASS_NAME, 'controls-btn')
            
            # Wait until the '50 Rows' button in the dropdown is visible and clickable, then click it
            self.click_button(By.XPATH, "//button[@title='Show 50 Rows']")
            time.sleep(10)

            # Scrape the rows
            page_soup = self.parse_page_content()
            tbody = page_soup.find('tbody')
            rows = tbody.find_all('tr', class_='svelte-eurwtr')
            result = []
            for row in rows:
                columns = row.find_all('td')
                data = [col.text.strip() for col in columns]
                result.append(data)
        except:
            raise

        return result

    def scrape_premarket_gainers(self):
        self.set_url(base_url, MarketMovers.PREMARKET, PremarketOptions.GAINERS)
        self.open_url()
        try:
            result = self._extract_table_rows()
            self.close()
        except:
            raise Exception('Failed to retrieve the data from table with pre-market gainers')
        
        return result



    def scrape_premarket_losers(self):
        raise NotImplementedError("This method needs to be implemented.")

    def scrape_aftermarket_gainers(self):
        self.set_url(base_url, MarketMovers.AFTER_HOURS, AfterHoursOptions.GAINERS)
        self.open_url()
        try:
            result = self._extract_table_rows()
            self.close()
        except:
            raise Exception('Failed to retrieve the data from table with after hours gainers')
        
        return result
    
    def _scrape_news(self, page_soup):
        # Find all divs with the specified class
        divs = page_soup.find_all('div', class_='flex flex-col')
        try:
            result = []
            for div in divs:
                # Extract the headline
                headline = div.find('h3').text.strip()
                # Extract the link
                link = div.find('a')['href']
                # Extract the description
                description = div.find('p').text.strip()
                # Extract the metadata (time and source)
                metadata = div.find('div', class_='mt-1 text-sm text-faded sm:order-1 sm:mt-0').text.strip()
                
                article_data = {
                    'headline': headline,
                    'link': link,
                    'description': description,
                    'metadata': metadata
                }
                result.append(article_data)
        except:
            raise Exception('Failed to retrieve market news')
        
        return result

    def _click_stock_overview_link(self):
        try:
            # Click the "Overview" link by locating it using XPath or any other preferred method
            overview_link = self.driver.find_element(By.XPATH, '//a[@data-title="Overview"]')
            overview_link.click()
        except Exception as e:
            raise Exception(f"Failed to click on the Overview link: {e}")

    def _get_overview_table(self, soup):
        div_elements = soup.find_all('div')

        # Iterate through each <div> to find the first one that contains exactly two <table> elements
        for div in div_elements:
            tables = div.find_all('table')
            if len(tables) == 2:
                target_div = div
                break
        
        result = {}
        try:
            tables = target_div.find_all('table')

            # Iterate over all rows in the table's tbody
            for table in tables:
                for row in table.find_all('tr'):
                    # Find all td elements in the row
                    cells = row.find_all('td')
                    if len(cells) == 2:  # Ensure there are exactly 2 columns
                        key = cells[0].get_text(strip=True)  # First column as key
                        value = cells[1].get_text(strip=True)  # Second column as value
                        result[key] = value  # Store the pair in the dictionary
        except:
            return None

        return result
    
    def _get_about_data(self, soup):
        # Find the <div> elements with class 'grid' and that have six child <div> elements
        grid_divs = soup.find_all('div', class_='grid')

        # Iterate over the grid <div> elements to find the one with exactly six child <div> elements
        target_div = None
        for div in grid_divs:
            child_divs = div.find_all('div', class_='col-span-1')
            if len(child_divs) == 6:
                target_div = div
                break

        result = {}
        try:
            for child_div in target_div.find_all('div', class_='col-span-1'):
                key = child_div.find('span').get_text(strip=True)
                value_tag = child_div.find('a')
                if value_tag:
                    value = value_tag.get_text(strip=True)
                else:
                    value = child_div.find_all('span')[-1].get_text(strip=True)
                result[key] = value
        except:
            return None

        return result

    def scrape_market_news(self):
        self.set_url(base_url, News.MARKETS)
        self.open_url()
        page_soup = self.parse_page_content()
        return self._scrape_news(page_soup)

    def scrape_all_stocks_news(self):
        self.set_url(base_url, News.ALL_STOCKS)
        self.open_url()
        page_soup = self.parse_page_content()
        return self._scrape_news(page_soup)
    
    def scrape_press_release_news(self):
        self.set_url(base_url, News.PRESS_RELEASES)
        self.open_url()
        page_soup = self.parse_page_content()
        return self._scrape_news(page_soup)
    
    def scrape_stock_data(self, stock_symbol: str):
        """
        Scrape the data for a specific stock identified by its symbol.
        """
        # Set the URL for the stock
        self.set_stock_url(stock_symbol)
        
        # Open the stock's page
        self.open_url()
        
        # Parse the page content
        page_soup = self.parse_page_content()
        
        try:
            # Example: Find the current stock price (you may need to adjust the selectors)
            stock_price_elem = page_soup.select_one('.text-4xl.font-bold')
            if not stock_price_elem:
                raise Exception(f"Failed to retrieve the Price for stock {stock_symbol}")
            stock_price = stock_price_elem.get_text(strip=True)

            # Overview tab
            self._click_stock_overview_link()

            # table = page_soup.find('table', {'data-test': 'overview-info'})
            overview_data = self._get_overview_table(page_soup)

            about_data = self._get_about_data(page_soup)

            news_data = self._scrape_news(page_soup)

        except Exception as e:
            raise Exception(f"Failed to retrieve data for stock {stock_symbol}: {e}")
        finally:
            self.close()
            result = {
                'price': stock_price,
                'overview': overview_data,
                'about': about_data,
                'news': news_data
            }
        
        return result
    
    def scrape_earnings(self):
        self.set_url(base_url, Stocks.EARNINGS)
        self.open_url()

        # Parse the page content
        page_soup = self.parse_page_content()

        # get current time in format "Aug 15, 2024"
        current_date = datetime.now()
        formatted_date = current_date.strftime("%b %d, %Y")

        # Click on button 'Daily'
        self.click_button(By.XPATH, "//button[text()='Daily']")


        # Select current date 
        self.click_button(By.XPATH, f"//button[.//div[contains(text(), '{formatted_date}')]]")

        # Parse the page content
        page_soup = self.parse_page_content()

        try:
            # Find the table 
            table = page_soup.find('table')
    
            # Extract headers
            headers = [th.get_text(strip=True) for th in table.find_all('th')]

            # Extract rows
            rows = []
            for tr in table.find_all('tr')[1:]:  # Skip the header row
                cells = tr.find_all('td')
                row = {headers[i]: cells[i].get_text(strip=True) for i in range(len(cells))}
                rows.append(row)

        except:
            raise Exception(f"Can't get Earnings data for that date {formatted_date}")

        return rows
