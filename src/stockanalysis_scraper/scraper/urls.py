from .enums import MarketMovers, PremarketOptions, AfterHoursOptions, \
    LosersOptions, ActiveOptions, GainersOptions, News, Stocks

page_options = {
    MarketMovers.PREMARKET: {
        PremarketOptions.MOVERS: '',
        PremarketOptions.GAINERS: 'gainers/',
        PremarketOptions.LOSERS: 'losers/',
    },
    MarketMovers.AFTER_HOURS: {
        AfterHoursOptions.MOVERS: '',
        AfterHoursOptions.GAINERS: 'gainers/',
        AfterHoursOptions.LOSERS: 'losers/',
    },
    MarketMovers.ACTIVE: {
        ActiveOptions.TODAY: '',
    },
    MarketMovers.LOSERS: {
        LosersOptions.TODAY: '',
        LosersOptions.WEEK: 'week/',
        LosersOptions.MONTH: 'month/',
        LosersOptions.YTD: 'ytd/',
        LosersOptions.YEAR: 'year/',
        LosersOptions.THREE_YEARS: '3y/',
        LosersOptions.FIVE_YEARS: '5y/',

    },
    MarketMovers.GAINERS: {
        GainersOptions.TODAY: '',
        GainersOptions.WEEK: 'week/',
        GainersOptions.MONTH: 'month/',
        GainersOptions.YTD: 'ytd/',
        GainersOptions.YEAR: 'year/',
        GainersOptions.THREE_YEARS: '3y/',
        GainersOptions.FIVE_YEARS: '5y/',
    },
    News.MARKETS: {},
    News.ALL_STOCKS: {},
    News.PRESS_RELEASES: {},
    Stocks.SCREENER: {},
    Stocks.EARNINGS: {},
    Stocks.INDUSTRY: {},
    Stocks.LIST: {},
    Stocks.ANALYSTS: {},
    Stocks.TOP_STOCKS: {},
    Stocks.ACTIONS: {}
}
