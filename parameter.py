stock_directory = 'input_stock/'

# stock info : Name, Allocation Ratio in %
stock_info = {'TQQQ':100}
purchase_day = 40
sell_profit_percent = +10

investment_dollar = 10000

skip_historical_data_download = True
historical_data_url_prefix = 'https://query1.finance.yahoo.com/v7/finance/download/'
historical_data_url_suffix = '?period1=0&period2=2000000000&interval=1d&events=history&includeAdjustedClose=true'

stock_back_test_period = {
    'start': {
        'year':2020,
        'month':2,
        'day':1
    },
    'end' : {
        'year':2022,
        'month':12,
        'day':31
    }
}