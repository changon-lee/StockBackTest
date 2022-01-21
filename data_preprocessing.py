from parameter import *
import urllib.request

def load_stock_historical_data():
    for stock_name in stock_list:
        print(historical_data_url_prefix + stock_name + historical_data_url_suffix)
        url = historical_data_url_prefix + stock_name + historical_data_url_suffix
        path = 'input_stock/' + stock_name + '.csv'
        urllib.request.urlretrieve(url, path)
