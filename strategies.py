from engine import Engine, Strategy
import yfinance as yf
 
class BuyAndSellSwitch(Strategy):
    def execute(self):
        if self.position_size == 0:
            self.buy('AAPL', 1)
        else:
            self.sell('AAPL', 1)

if __name__ == "__main__":

    data = yf.Ticker('AAPL').history(start='2022-12-01', end='2022-12-31', interval='1d')
    e = Engine()
    e.add_data(data)
    e.add_strategy(BuyAndSellSwitch())
    e.run()  

