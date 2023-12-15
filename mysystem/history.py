import pandas as pd

class history:
    def __init__(self):
        # indices are dates
        self.hold_history = pd.DataFrame(index=[], columns=['cash', 'stock', 'total_value'])
        
        self.net_values = []
        self.order_history = []
        # indices are dates, values are return ratios
        self.return_history = pd.DataFrame(index=[], columns=['ratio']) 
