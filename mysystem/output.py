import pandas as pd
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import statistics as stats
import numpy as np
import yfinance as yf

class output:
    def __init__(self, history):
        self.history = history

    def plot_output(self):
        # Net value curve
        date_list = self.history.return_history.index.tolist()
        plt.title("Net Value Curve", fontsize=14)
        plt.plot(date_list, self.history.net_values, c='r', label='Net Value Curve')
        plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(5))
        plt.show()

        # Excess returns
        index_data = yf.download("000001.SS", start="2020-01-01", end="2022-12-31")
        index_dict = {'date': [], 'close': []}

        for date in date_list:
            index_dict['date'].append(date)
            index_dict['close'].append(index_data.loc[date]['Close'])

        index_dict = pd.DataFrame(index_dict)
        index_dict['date'] = pd.to_datetime(index_dict['date'])
        index_dict.set_index('date', inplace=True)
        benchmark_return = index_dict['close'].pct_change()
        benchmark_return.fillna(0, inplace=True)

        return_list = self.history.return_history.values.flatten()
        excess_returns = np.array(return_list) - np.array(benchmark_return)

        plt.title("Excess Returns", fontsize=14)
        plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(5))
        plt.plot(date_list, excess_returns, c='b', label='Excess Returns')
        plt.show()
        
        # Annualized return
        annualized_return = (1 + np.array(return_list).mean())**252 - 1
        print('Annualized return is', annualized_return)

        # Annual volatility
        annualized_volatility = stats.stdev(return_list) * np.sqrt(252)
        print('Annualized volatility is', annualized_volatility)

        # Sharpe ratio
        risk_free = stats.mean(benchmark_return)
        sharpe_ratio = (return_list[-1] - risk_free) / stats.stdev(return_list)
        print('Sharpe ratio is', sharpe_ratio)

        # Maximum drawdown
        peak_values = pd.Series(self.history.net_values).cummax()
        drawdown = (peak_values - self.history.net_values) / peak_values
        max_drawdown = drawdown.max()
        print('Maximum drawdown is', max_drawdown)

    def save_order_history(self):
        output_path = './newdata/history_order.csv'
        order_history = self.history.order_history
        output_df = pd.DataFrame(order_history, 
                                 columns=['Date', 'Stock', 'Volume', 'Price', 'Action'])
        output_df.to_csv(output_path, index=True, header=True)

    def save_hold_history(self):
        output_path = './newdata/history_hold.csv'
        hold_history = self.history.hold_history
        hold_history.to_csv(output_path, index=True, header=True)