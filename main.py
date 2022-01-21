from data_preprocessing import load_stock_historical_data, read_stock_historical_data, set_back_test_period

if __name__ == '__main__':
    file_list = load_stock_historical_data()

    for file_name in file_list:
        df = read_stock_historical_data(file_name)
        df = set_back_test_period(df)


