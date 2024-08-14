# Stock Analysis Scraper

This project is a Python-based web scraper designed to extract relevant stock information from the Stock Analysis website. It utilizes `BeautifulSoup` to parse HTML content and extract specific data points, such as market capitalization, revenue, industry, sector, and more. Additionally, it can extract pre-market gainers, after-hours gainers, and all news articles related to stocks.

## Features

-   Extracts stock information including:
    -   Market Capitalization
    -   Revenue (TTM)
    -   Net Income (TTM)
    -   Shares Outstanding
    -   EPS (TTM)
    -   P/E Ratio
    -   Dividend Information
-   Extracts profile details such as:
    -   Industry
    -   Sector
    -   IPO Date
    -   Number of Employees
    -   Stock Exchange
    -   Ticker Symbol
-   Extracts lists of:
    -   **Pre-Market Gainers**: Stocks with the highest gains during pre-market trading.
    -   **After-Hours Gainers**: Stocks with the highest gains during after-hours trading.
    -   **All News**: Recent news articles related to the stock market and specific stocks.
-   Outputs the extracted data as a dictionary for easy integration with other applications or storage solutions.

## Prerequisites

Before running the scraper, ensure you have the following installed:

-   Python 3.6+
-   `BeautifulSoup4`
-   `lxml` (optional but recommended for faster HTML parsing)

You can install the required Python packages using `pip`:

```bash
pip install beautifulsoup4 lxml
```
