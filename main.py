
import pandas as pd
from tqdm import tqdm
import yfinance as yf

class Engine():
    """
    Main object used to run backtests
    """
    def __init__(self, initial_cash = 100_000):

        self.strategy = None
        self.cash = initial_cash
        self.data = None
        self.current_idx = None

    def add_data(self, data:pd.DataFrame):
        # Add OHLC data to the engine

        self.data = data

    def add_strategy(self, strategy):
        # Add a strategy to the engine

        self.strategy = strategy

    def run(self):
            # Processing items

            self.strategy.data = self.data

            for idx in tqdm(self.data.index):
                self.current_idx = idx
                self.strategy.current_idx = self.current_idx

                self._fill_orders()

                # Run the strategy on the current bar
                # self.strategy.on_bar()
                print(idx)

    def _fill_orders(self):
        # Fill orders from the previou period

        pass


    def _get_stats(self):
        metrics = {}

        # Calculate the total return
        current_close = self.data.loc[self.current_idx]['Close']
        current_value = current_close * self.strategy.position_size + self.cash
    
        total_return = 100 * ((current_value / self.initial_cash) - 1)
        metrics['total_return'] = total_return
    
        return metrics


class Strategy():
    """
    Handle the execution logic of the trading strategies
    """
    def __init__(self):
        self.current_idx = None
        self.data = None
        self.orders = []
        self.trades = []

    def buy(self,ticker,size=1):

        # appends a buy order object
        self.orders.append(
            Order(
                ticker = ticker,
                side = 'buy',
                size = size,
                idx = self.current_idx
            ))

    def sell(self,ticker,size=1):

        # appends a sell order object 
        self.orders.append(
            Order(
                ticker = ticker,
                side = 'sell',
                size = -size,
                idx = self.current_idx
            ))
        
    @property
    def position_size(self):
        # Returns the total size of the executed trades
        return sum([t.size for t in self.trades])
        
    def on_bar(self):
        """
        This method will be overriden by our strategies.
        """
        pass

    

class Order():
    """
    When buying or selling, we first create an order object.
    """
    def __init__(self, ticker, size, side, idx):
        self.ticker = ticker
        self.side = side
        self.size = size
        self.type = 'market'
        self.idx = idx
        

class Trade():
    """
    Trade objects are created when an order is filled.
    """
    def __init__(self, ticker,side,size,price,type,idx):
        self.ticker = ticker
        self.side = side
        self.price = price
        self.size = size
        self.type = type
        self.idx = idx

if __name__ == "__main__":
    
    data = yf.Ticker('AAPL').history(start='2020-01-01', end='2022-12-31', interval='1d')

    e = Engine()
    e.add_data(data)
    e.add_strategy(Strategy())
    e.run() 

