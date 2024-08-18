from enum import Enum


class Stocks(Enum):
    SCREENER = 'stocks/screener/'
    EARNINGS = 'stocks/earnings-calendar/'
    INDUSTRY = 'stocks/industry/'
    LIST = 'list/'
    ANALYSTS = 'analysts/'
    TOP_STOCKS = 'analysts/top-stocks/'
    ACTIONS = 'actions/'


class MarketMovers(Enum):
    PREMARKET = 'markets/premarket/'
    AFTER_HOURS = 'markets/afterhours/'
    ACTIVE = 'markets/active/'
    LOSERS = 'markets/losers/'
    GAINERS = 'markets/gainers/'


class PremarketOptions(Enum):
    MOVERS = ''
    GAINERS = 'gainers/'
    LOSERS = 'losers/'


class AfterHoursOptions(Enum):
    MOVERS = ''
    GAINERS = 'gainers/'
    LOSERS = 'losers/'


class ActiveOptions(Enum):
    TODAY = ''


class LosersOptions(Enum):
    TODAY = ''
    WEEK = 'week/'
    MONTH = 'month/'
    YTD = 'ytd/'
    YEAR = 'year/'
    THREE_YEARS = '3y/'
    FIVE_YEARS = '5y/'


class GainersOptions(Enum):
    TODAY = ''
    WEEK = 'week/'
    MONTH = 'month/'
    YTD = 'ytd/'
    YEAR = 'year/'
    THREE_YEARS = '3y/'
    FIVE_YEARS = '5y/'


class News(Enum):
    MARKETS = 'news/'
    ALL_STOCKS = 'news/all-stocks/'
    PRESS_RELEASES = 'news/press-releases/'

