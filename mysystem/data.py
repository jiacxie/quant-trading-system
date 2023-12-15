import pandas as pd
from datetime import datetime

class data:
    def __init__(self, data_all, date_all):
        self.data_all = data_all
        self.date_all = date_all
    
    def get_data_all(path):
        income_data = pd.read_feather(path, columns=None, use_threads=True)
        income_data.dropna(inplace=True)
        income_data.dropna(axis=1, inplace=True)
        income_data['date'] = pd.to_datetime(income_data['date']).dt.date.astype(str)

        grouped_data = income_data.groupby('date')  # grouping the data by date

        data_all = {}
        for date, group in grouped_data:  # Processing each group
            result = group.drop(columns=['date']).set_index('stk_id', inplace=False)
            data_all[date] = result

        return data_all
    
    def get_date_all(data_all, start_date, end_date):
        date = list(data_all.keys())
        date_all = date[date.index(start_date):date.index(end_date)+1]
        return date_all
    
    # the default strategy is to accept all valid stock as the buylist
    # please modify this function to have different ways in selecting stocks
    def generate_buy_list(data_all, start_date, end_date):
        buy_set = set(data_all[start_date].index)
        start_time = datetime.strptime(start_date, '%Y-%m-%d')
        end_time = datetime.strptime(end_date, '%Y-%m-%d')
        for date in data_all.keys():
            date_time = datetime.strptime(start_date, '%Y-%m-%d')
            if date_time < start_time:
                continue
            elif date_time > end_time:
                break
            buy_set &= set(data_all[date].index)
        buy_list = list(buy_set)
        return buy_list
    
    def get_data(self, date, stock, index):
        return self.data_all[date].loc[stock][index]
    
    def get_date(self, date_get, i):
        return self.date_all[self.date_all.index(date_get) + i]