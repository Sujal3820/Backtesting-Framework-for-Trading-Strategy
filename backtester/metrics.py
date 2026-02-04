import numpy as np
import pandas as pd

def sharpe_ratio(returns, risk_free_rate=0.0):
    excess_returns = returns - risk_free_rate
    return np.sqrt(252) * excess_returns.mean() / excess_returns.std()


def max_drawdown(equity_curve):
    roll_max = np.maximum.accumulate(equity_curve)
    drawdown = (equity_curve - roll_max) / roll_max
    return drawdown.min()


def total_return(equity_curve):
    return (equity_curve[-1] / equity_curve[0]) - 1
