from .enums import Pages, PremarketOptions, AfterHoursOptions, \
    LosersOptions, ActiveOptions, GainersOptions, News

page_options = {
    Pages.PREMARKET: {
        PremarketOptions.MOVERS: '',
        PremarketOptions.GAINERS: 'gainers/',
        PremarketOptions.LOSERS: 'losers/',
    },
    Pages.AFTER_HOURS: {
        AfterHoursOptions.MOVERS: '',
        AfterHoursOptions.GAINERS: 'gainers/',
        AfterHoursOptions.LOSERS: 'losers/',
    },
    Pages.ACTIVE: {
        ActiveOptions.TODAY: '',
    },
    Pages.LOSERS: {
        LosersOptions.TODAY: '',
        LosersOptions.WEEK: 'week/',
        LosersOptions.MONTH: 'month/',
        LosersOptions.YTD: 'ytd/',
        LosersOptions.YEAR: 'year/',
        LosersOptions.THREE_YEARS: '3y/',
        LosersOptions.FIVE_YEARS: '5y/',

    },
    Pages.GAINERS: {
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
    News.PRESS_RELEASES: {}
}
