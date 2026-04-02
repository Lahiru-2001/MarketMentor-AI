def analyze_market_trend(price_series: list) -> str:
    # Check if there are at least 5 price values available
    # because trend analysis needs minimum recent data points
    if len(price_series) < 5:
        return "Insufficient data"

    # Take the last 5 prices from the list for recent trend analysis
    recent = price_series[-5:]

    # If the latest price is greater than the first price
    # in the recent 5 values, market is moving upward
    if recent[-1] > recent[0]:
        return "Uptrend"

    # If the latest price is lower than the first price
    # in the recent 5 values, market is moving downward
    elif recent[-1] < recent[0]:
        return "Downtrend"

    # If prices are unchanged overall, market is sideways
    return "Sideways"