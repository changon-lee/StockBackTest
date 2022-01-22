from parameter import *
import urllib.request
import os
import pandas as pd
import datetime
from datetime import date

def load_stock_historical_data():
    file_list = list()
    for stock_name in stock_info.keys():
        url = historical_data_url_prefix + stock_name + historical_data_url_suffix
        path = stock_directory + stock_name + '.csv'
        if not skip_historical_data_download:
            if not os.path.exists(stock_directory):
                os.mkdir(stock_directory)
            urllib.request.urlretrieve(url, path)
        file_list.append(path)

    return file_list

def read_stock_historical_data(file_name):
    return pd.read_csv(file_name, thousands = ',')

def search_index(date_list, year, month, day):
    pivot_date = date(year,month,day)

    for idx, line in enumerate(date_list):
        _year, _month, _day = list(map(int,line.split('-')))
        if date(_year, _month, _day) >= pivot_date:
            return idx

    return len(date_list)

def set_back_test_period(df):
    start_idx = search_index(df['Date'],
                             stock_back_test_period['start']['year'],
                             stock_back_test_period['start']['month'],
                             stock_back_test_period['start']['day'])

    end_idx = search_index(df['Date'],
                             stock_back_test_period['end']['year'],
                             stock_back_test_period['end']['month'],
                             stock_back_test_period['end']['day'])

    return df[start_idx:end_idx]

def preprocessing(df):
    df['Date'] = df['Date'].apply(lambda x : datetime.datetime.strptime(x, '%Y-%m-%d'))
    df['Open'] = df['Open'].astype(float)
    df['High'] = df['High'].astype(float)
    df['Low'] = df['Low'].astype(float)
    df['Close'] = df['Close'].astype(float)
    df['Adj Close'] = df['Adj Close'].astype(float)
    df['Volume'] = df['Volume'].astype(int)

    return df