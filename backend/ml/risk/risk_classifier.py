import numpy as np

def predict_risk(prices: list) -> str:
    """
    Predicts the risk level of a stock based on its price volatility.

    Parameters:
    -----------
    prices : list
        A list of historical stock prices (floats or integers).

    Returns:
    --------
    str
        A risk category: "Low Risk", "Medium Risk", or "High Risk".

    Method:
    -------
    - If the list has fewer than 5 prices, it defaults to "Medium Risk".
    - Computes daily returns as the percentage change between consecutive prices.
    - Calculates volatility as the standard deviation of returns.
    - Categorizes risk based on volatility thresholds:
        < 0.01   -> Low Risk
        0.01-0.03 -> Medium Risk
        > 0.03   -> High Risk
    """

    # If there are too few prices, assume Medium Risk due to insufficient data
    if len(prices) < 5:
        return "Medium Risk"

    # Calculate returns: percentage change between consecutive prices
    returns = np.diff(prices) / prices[:-1]

    # Calculate volatility as standard deviation of returns
    volatility = np.std(returns)

    # Determine risk category based on volatility thresholds
    if volatility < 0.01:
        return "Low Risk"
    elif volatility < 0.03:
        return "Medium Risk"
    else:
        return "High Risk"