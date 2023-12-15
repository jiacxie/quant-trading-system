import pandas as pd
import numpy as np
import statistics as stats 

class strategy:
    def __init__(self, data, portfolio, buy_list, start_date):
        self.data = data
        self.data_all = data.data_all
        self.date_all = data.date_all
        self.me = portfolio
        self.buy_list = buy_list
        self.start_date = start_date

    # five days reverse strategy
    def five_days_reverse(self, date):
        reverse_buy_list = []
        reverse_sell_list = []

        # check sell signals
        for stock in self.buy_list:
            total_price = 0
            for i in range(1, 6):
                date_i = self.data.get_date(date, -i)
                total_price += self.data.get_data(date_i, stock, 'close')
            average_price = total_price / 5
            current_price = self.data.get_data(date, stock, 'close')
            if current_price < average_price:
                reverse_buy_list.append(stock)

        # check buy signals
        for stock in self.me.stock_hold.index:
            total_price = 0
            for i in range(1, 6):
                date_i = self.data.get_date(date, -i)
                total_price += self.data.get_data(date_i, stock, 'close')
            average_price = total_price / 5
            current_price = self.data.get_data(date, stock, 'close')
            if current_price > average_price:
                reverse_sell_list.append(stock)

        # buy
        for stock_buy in reverse_buy_list:
            price_stock_buy = self.data.get_data(date, stock_buy, 'close')
            num = (self.me.cash - 1000) / len(reverse_buy_list) / 100 // price_stock_buy * 100
            self.me.buy(stock_buy, num, date)

        # sell
        for stock_sell in reverse_sell_list:
            num_to_sell = self.me.stock_hold.loc[stock_sell]['num']
            self.me.sell(stock_sell, num_to_sell, date)