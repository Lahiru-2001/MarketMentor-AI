def analyze_market_trend(price_series: list) -> str:
    if len(price_series) < 5:
        return "Insufficient data"

    recent = price_series[-5:]
    if recent[-1] > recent[0]:
        return "Uptrend"
    elif recent[-1] < recent[0]:
        return "Downtrend"
    return "Sideways"
