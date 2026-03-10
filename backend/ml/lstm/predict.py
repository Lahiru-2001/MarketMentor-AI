import numpy as np

def predict_price(prices: list) -> float:
    """
    Real-time statistical forecast using linear regression
    """
    if len(prices) < 5:
        return prices[-1]

    x = np.arange(len(prices))
    y = np.array(prices)

   
    slope, intercept = np.polyfit(x, y, 1)

    next_index = len(prices)
    prediction = slope * next_index + intercept

    return float(round(prediction, 2))
