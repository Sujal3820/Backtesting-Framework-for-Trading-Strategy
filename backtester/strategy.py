
from abc import ABC, abstractmethod
import pandas as pd

class Strategy(ABC):
    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        pass


class MovingAverageStrategy(Strategy):
    def __init__(self, short_window: int, long_window: int):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        signals = pd.DataFrame(index=data.index)
        signals["signal"] = 0

        signals["short_ma"] = data["Close"].rolling(self.short_window).mean()
        signals["long_ma"] = data["Close"].rolling(self.long_window).mean()

        signals.loc[
            signals["short_ma"] > signals["long_ma"], "signal"
        ] = 1

        signals["positions"] = signals["signal"].diff()
        return signals

# class Strategy(ABC):
#     @abstractmethod
#     def generate_signals(self, data: pd.DataFrame) -> pd.Series:
#         pass

# class MovingAverageStrategy(Strategy):
#     def __init__(self, short_window=20, long_window=50):
#         self.short_window = short_window
#         self.long_window = long_window

#     def generate_signals(self, data):
#         data['short_ma'] = data['Close'].rolling(self.short_window).mean()
#         data['long_ma'] = data['Close'].rolling(self.long_window).mean()

#         signals = pd.Series(0, index=data.index)
#         signals[data['short_ma'] > data['long_ma']] = 1
#         signals[data['short_ma'] < data['long_ma']] = -1
#         return signals
