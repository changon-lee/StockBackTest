from data_preprocessing import load_stock_historical_data, read_stock_historical_data, set_back_test_period, preprocessing
from investment import scale_trading, dollar_cost_averaging
from parameter import stock_info

if __name__ == '__main__':
    file_list = load_stock_historical_data()

    for stock_name, file_name in zip(stock_info.keys(), file_list):
        df = read_stock_historical_data(file_name)
        df = set_back_test_period(df)
        df = preprocessing(df)

        #Scale Trading
        scale_trading(df, stock_name)
        dollar_cost_averaging(df, stock_name)
