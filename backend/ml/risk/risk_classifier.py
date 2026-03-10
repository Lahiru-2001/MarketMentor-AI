import numpy as np

def predict_risk(prices: list) -> str:
    """
    Risk based on volatility (standard deviation)
    """

    if len(prices) < 5:
        return "Medium Risk"

    returns = np.diff(prices) / prices[:-1]
    volatility = np.std(returns)

    if volatility < 0.01:
        return "Low Risk"
    elif volatility < 0.03:
        return "Medium Risk"
    else:
        return "High Risk"
