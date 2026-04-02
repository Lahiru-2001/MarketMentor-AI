import numpy as np   # Import NumPy library for numerical operations

def calculate_rsi(prices, period=14):
    # Check if there is enough price data to calculate RSI
    # RSI needs at least (period + 1) values because diff() reduces one value
    if len(prices) < period + 1:
        return 50   # Return neutral RSI if not enough data

    # Calculate price changes between consecutive days
    deltas = np.diff(prices)

    # Calculate average gains:
    # Select only positive changes and divide total by period
    gains = deltas[deltas > 0].sum() / period

    # Calculate average losses:
    # Select only negative changes, convert to positive, divide by period
    losses = -deltas[deltas < 0].sum() / period

    # If there are no losses, RSI is maximum (100)
    if losses == 0:
        return 100

    # Calculate Relative Strength (RS)
    rs = gains / losses

    # Apply RSI formula
    rsi = 100 - (100 / (1 + rs))

    # Return RSI rounded to 2 decimal places
    return round(rsi, 2)