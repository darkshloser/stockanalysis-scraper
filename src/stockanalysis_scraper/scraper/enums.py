from enum import Enum

class Pages(Enum):
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

