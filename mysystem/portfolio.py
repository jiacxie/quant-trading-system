import pandas as pd

class portfolio:
    def __init__(self, cash, date, commission, history, data):
        self.cash = cash
        self.total_value = cash
        self.stock_hold = pd.DataFrame(index=[], columns=['num', 'price']) # indices are stock ids
        self.stock_value = 0
        self.date = date
        self.commision = commission
        self.history = history
        self.data = data

    def buy(self, stock, num, date):
        price = self.data.get_data(date, stock, 'close')
        self.cash = self.cash - num * price - num * price * self.commision
        self.stock_hold.loc[stock] = {'num' : num, 'price' : price}
        self.stock_value = sum(self.stock_hold['num'] * self.stock_hold['price'])
        self.total_value = self.cash + self.stock_value
        self.history.order_history.append([date, stock, num, price, 'buy'])

    def sell(self, stock, num, date):
        price = self.data.get_data(date, stock, 'close')
        self.cash = self.cash + num * price - num * price * self.commision
        self.stock_hold.drop(index=stock, inplace=True) # will be re-added in df when buying again
        self.stock_value = sum(self.stock_hold['num'] * self.stock_hold['price'])
        self.total_value = self.cash + self.stock_value
        self.history.order_history.append([date, stock, num, price, 'sell'])

    def sell_all(self, date):
        stocks_to_sell = self.stock_hold.index.tolist()
        if len(stocks_to_sell) > 0:
            for stock in stocks_to_sell:
                self.sell(stock, self.stock_hold.loc[stock]['num'], date)
