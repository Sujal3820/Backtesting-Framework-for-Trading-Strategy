import pandas as pd

class Backtester:
    def __init__(self, data, strategy, initial_capital=100000):
        self.data = data
        self.strategy = strategy
        self.initial_capital = initial_capital

    def run(self):
        signals = self.strategy.generate_signals(self.data)

        portfolio = pd.DataFrame(index=self.data.index)
        portfolio["price"] = self.data["Close"]
        portfolio["holdings"] = signals["signal"] * portfolio["price"]
        portfolio["cash"] = self.initial_capital - (
            signals["positions"] * portfolio["price"]
        ).cumsum()
        portfolio["equity"] = portfolio["cash"] + portfolio["holdings"]

        return portfolio
