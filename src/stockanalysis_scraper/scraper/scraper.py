import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from .config import get_settings
from .enums import Pages, PremarketOptions, AfterHoursOptions, ActiveOptions, \
LosersOptions, GainersOptions, News
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

    def set_url(self, base_url: str, page: Pages, option=None):
        url = base_url + page.value
        if option and option in page_options.get(page, {}):
            url += page_options[page].get(option,'')
        self.url = url

    def open_url(self):
        self.driver.get(self.url)
        self.driver.implicitly_wait(10)  # Wait for JavaScript to render

    def parse_page_content(self):
        html = self.driver.page_source
        return BeautifulSoup(html, 'html.parser')

    def close(self):
        self.driver.quit()

    def click_button(self, by: By, value: str):
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((by, value))
        )
        button.click()

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
        self.set_url(base_url, Pages.PREMARKET, PremarketOptions.GAINERS)
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
        self.set_url(base_url, Pages.AFTER_HOURS, AfterHoursOptions.GAINERS)
        self.open_url()
        try:
            result = self._extract_table_rows()
            self.close()
        except:
            raise Exception('Failed to retrieve the data from table with after hours gainers')
        
        return result
    
    def _scrape_news(self, news: News):
        self.set_url(base_url, news)
        self.open_url()
        page_soup = self.parse_page_content()

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

    def scrape_market_news(self):
        return self._scrape_news(News.MARKETS)

    def scrape_all_stocks_news(self):
        return self._scrape_news(News.ALL_STOCKS)
    
    def scrape_press_release_news(self):
        return self._scrape_news(News.PRESS_RELEASES)
