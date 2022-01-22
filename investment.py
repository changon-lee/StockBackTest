from parameter import *
import pandas as pd
import plotly.offline as plyo
import cufflinks as cf

class TradingModel:
    def __init__(self, _model_name, _stock_name):
        self.model_name = _model_name
        self.stock_name = _stock_name
        self.initial_input_dollar = 0
        self.total_stock_count = 0
        self.valuation = 0
        self.available_deposit = 0
        self.stock_buy_average_price = 0

        self.elapsed_day = 0
        self.profit_rate = 0

        self.open_price_log = list()
        self.initial_input_dollar_log = list()
        self.valuation_log = list()
        self.profit_rate_log = list()

    def deposit(self, dollar):
        self.initial_input_dollar += dollar
        self.available_deposit += dollar

    def add_log(self, open_price):
        self.valuation_log.append(self.valuation)
        self.initial_input_dollar_log.append(self.initial_input_dollar)
        self.open_price_log.append(open_price)
        self.profit_rate_log.append(((self.valuation / self.initial_input_dollar) - 1) * 100)

    def calculate_profit(self, profit_price, input_dollar = 0):
        if input_dollar == 0:
            input_dollar = self.initial_input_dollar
        self.stock_buy_average_price = (input_dollar - self.available_deposit) / self.total_stock_count
        self.profit_rate = ((profit_price / self.stock_buy_average_price) - 1) * 100

    def update_profit(self, profit_price, open_price):
        self.valuation = (open_price * self.total_stock_count) + self.available_deposit
        self.add_log(open_price)

        if self.total_stock_count == 0:
            return

        self.calculate_profit(profit_price)


    def buy_stock(self, deposit, buy_price):
        if self.available_deposit <= buy_price:
            return
        buy_stock_count = deposit // buy_price
        self.total_stock_count += buy_stock_count
        self.available_deposit -= buy_stock_count * buy_price

    def sell_stock(self, sell_price):
        self.available_deposit += self.total_stock_count * sell_price

    def print_result(self):
        print(' * ' + self.model_name)
        print('   * Stock Name : ' + self.stock_name)
        print('   * Total Input Dollar : %d' % self.initial_input_dollar)
        print('   * Total Output dollar : %f' % self.available_deposit)
        print('   * Profit : %f%%' % (((self.available_deposit / self.initial_input_dollar) - 1) * 100))

    def make_plot_dataframe(self, date_list):
        plot_df = pd.DataFrame({'Valuation': self.valuation_log,
                      'Input Dollar': self.initial_input_dollar_log,
                      'Open Price': self.open_price_log,
                      'Profit Rate': self.profit_rate_log},
                     index=date_list)

        return plot_df

    def plot_result(self, date_list):
        plot_df = self.make_plot_dataframe(date_list)

        layout = {
            'title': {'text': self.stock_name, 'font': {'family': 'consolas', 'size': 20, 'color': '#01579B'}},
            'xaxis': {'showticklabels': True, 'title': {'text': 'date', 'font': {'size': 10}}}
        }
        plyo.iplot(plot_df.iplot(asFigure=True, layout=layout))


class CostAveragingModel(TradingModel):
    def __init__(self, _stock_name):
        model_name = 'Cost Averaging Model'
        super().__init__(model_name, _stock_name)

    def buy_stock(self, buy_price):
        super().buy_stock(self.available_deposit, buy_price)

class ScaleTradingParam(TradingModel):
    def __init__(self, _stock_name):
        model_name = 'Scale Trading Model'
        super().__init__(model_name, _stock_name)
        self.number_of_purchase_day = 0
        self.dollar_per_day = 0
        self.input_dollar = 0
        self.sell_profit_percent = 0

        self.available_deposit_log = list()

    def set_dollar_per_day(self):
        self.dollar_per_day = self.available_deposit / self.number_of_purchase_day

    def set_number_of_purchase_day(self, _number_of_purchase_day):
        self.number_of_purchase_day = _number_of_purchase_day

    def set_sell_profit_percent(self, _sell_profit_percent):
        self.sell_profit_percent = _sell_profit_percent

    def get_dollar_per_day(self):
        return self.dollar_per_day

    def deposit(self, dollar):
        super().deposit(dollar)
        self.input_dollar += dollar

    def add_log(self, open_price):
        super().add_log(open_price)
        self.available_deposit_log.append(self.available_deposit)

    def calculate_profit(self, profit_price):
        super().calculate_profit(profit_price, self.input_dollar)

    def update_profit(self, high_price, open_price):
        super().update_profit(high_price, open_price)

        if self.profit_rate > self.sell_profit_percent:
            self.profit_rate = self.sell_profit_percent

    def model_restart(self):
        self.total_stock_count = 0
        self.elapsed_day = 0
        self.profit_rate = 0
        self.stock_buy_average_price = 0
        self.input_dollar = self.available_deposit
        self.set_dollar_per_day()

    def buy_stock(self, buy_price):
        super().buy_stock(self.dollar_per_day, buy_price)

    def sell_stock(self):
        sell_price = (1 + (self.profit_rate / 100)) * self.stock_buy_average_price
        super().sell_stock(sell_price)
        self.model_restart()

    def sell_timing_check(self):
        # if (self.profit_rate >= self.sell_profit_percent or
        #     self.elapsed_day >= self.number_of_purchase_day) and \
        #         self.total_stock_count != 0:
        if (self.profit_rate >= self.sell_profit_percent) and self.total_stock_count != 0:
            return True

        return False

    def next_day(self):
        self.elapsed_day += 1

    def make_plot_dataframe(self, date_list):
        plot_df = super().make_plot_dataframe(date_list)
        plot_df['Deposit'] = self.available_deposit_log

        return plot_df



def scale_trading(df, stock_name):
    model_param = ScaleTradingParam(stock_name)

    input_dollar = investment_dollar * (stock_info[stock_name] / 100)
    model_param.deposit(input_dollar)
    model_param.set_number_of_purchase_day(purchase_day)
    model_param.set_sell_profit_percent(sell_profit_percent)
    model_param.set_dollar_per_day()

    previous_month = 0
    dollar_input_per_month = 500
    for date, open_price, high_price, close_price in \
            zip(df['Date'], df['Open'], df['High'], df['Close']):
        if previous_month != date.month:
            previous_month = date.month
            model_param.deposit(dollar_input_per_month)
            model_param.set_number_of_purchase_day(purchase_day)
        model_param.update_profit(high_price, open_price)
        if model_param.sell_timing_check():
            model_param.sell_stock()
            continue

        model_param.buy_stock(close_price)
        model_param.next_day()

    model_param.sell_stock()
    model_param.print_result()
    model_param.plot_result(df['Date'])


def dollar_cost_averaging(df, stock_name):
    model_param = CostAveragingModel(stock_name)

    dollar_input_per_month = 1000
    model_param.deposit(dollar_input_per_month)

    previous_month = 0
    last_close_price = 0
    for date, open_price, high_price, close_price in \
            zip(df['Date'], df['Open'], df['High'], df['Close']):
        if previous_month != date.month:
            previous_month = date.month
            model_param.deposit(dollar_input_per_month)
        model_param.update_profit(close_price, open_price)
        model_param.buy_stock(close_price)
        last_close_price = close_price

    model_param.sell_stock(last_close_price)
    model_param.print_result()
    model_param.plot_result(df['Date'])





