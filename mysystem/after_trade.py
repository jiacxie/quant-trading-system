import pandas as pd

class after_trade:
    def __init__(self, portfolio, history, start_date, cash, data):
        self.me = portfolio
        self.history = history
        self.start_date = start_date
        self.cash = cash
        self.data = data

    def after_trade(self, date):
        current_stocks = self.me.stock_hold.index.tolist()
        num = self.me.stock_hold['num'].tolist()
        price = []
        for stock in current_stocks:
            price.append(self.data.get_data(date, stock, 'close'))
        stock_data = {'num': num, 'price': price}
        self.me.stock_hold = pd.DataFrame(stock_data, index=current_stocks)
        self.me.stock_value = sum(self.me.stock_hold['num'] * self.me.stock_hold['price'])
        self.me.total_value = self.me.cash + self.me.stock_value

        self.history.hold_history.loc[date] = {'cash': self.me.cash, 
                                               'stock': current_stocks, 
                                               'total_value': self.me.total_value}
        self.history.net_values.append(self.me.total_value)

        # record return rates
        if date == self.start_date:
            return_today = 0
        else:
            return_today = self.me.total_value / self.cash - 1
        self.history.return_history.loc[date] = {'ratio': round(return_today, 4)}