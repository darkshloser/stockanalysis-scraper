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
LosersOptions, GainersOptions
from .urls import page_options



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
            url += page_options[page][option]
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

    def scrape_premarket_gainers(self, base_url: str):
        self.set_url(base_url, Pages.PREMARKET, PremarketOptions.GAINERS)
        self.open_url()
        try:
            result = self._extract_table_rows()
            self.close()
        except:
            raise Exception('Failed to retrieve the data from table with pre-market gainers')
        
        return result



    def scrape_premarket_losers(self, base_url: str):
        raise NotImplementedError("This method needs to be implemented.")

    def scrape_aftermarket_gainers(self, base_url: str):
        self.set_url(base_url, Pages.AFTER_HOURS, AfterHoursOptions.GAINERS)
        self.open_url()
        try:
            result = self._extract_table_rows()
            self.close()
        except:
            raise Exception('Failed to retrieve the data from table with after hours gainers')
        
        return result
