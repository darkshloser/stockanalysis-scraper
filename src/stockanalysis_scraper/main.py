from scraper.config import get_settings
from scraper.scraper import StockAnalysis

def main():
    settings = get_settings()
    base_url = settings['base_url']
    
    scraper = StockAnalysis()
    
    # Scrape Premarket Movers
    movers_data = scraper.scrape_aftermarket_gainers(base_url)
    print(movers_data)

if __name__ == "__main__":
    main()