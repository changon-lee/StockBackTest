from parameter import *
import urllib.request
import os

def load_stock_historical_data():
    stock_directory_name = 'input_stock'
    for stock_name in stock_list:
        url = historical_data_url_prefix + stock_name + historical_data_url_suffix
        if not os.path.exists(stock_directory_name):
            os.mkdir(stock_directory_name)
        path = stock_directory_name + stock_name + '.csv'
        urllib.request.urlretrieve(url, path)
