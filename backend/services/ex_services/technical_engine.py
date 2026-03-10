import numpy as np

def calculate_rsi(prices, period=14):
    if len(prices) < period + 1:
        return 50

    deltas = np.diff(prices)
    gains = deltas[deltas > 0].sum() / period
    losses = -deltas[deltas < 0].sum() / period

    if losses == 0:
        return 100

    rs = gains / losses
    rsi = 100 - (100 / (1 + rs))
    return round(rsi, 2)
