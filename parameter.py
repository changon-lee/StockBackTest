stock_directory = 'input_stock/'
stock_list = ['TQQQ', 'QQQ', 'SQQQ']

historical_data_url_prefix = 'https://query1.finance.yahoo.com/v7/finance/download/'
historical_data_url_suffix = '?period1=0&period2=2000000000&interval=1d&events=history&includeAdjustedClose=true'

stock_back_test_period = {
    'start': {
        'year':2015,
        'month':1,
        'day':1
    },
    'end' : {
        'year':2021,
        'month':12,
        'day':31
    }
}