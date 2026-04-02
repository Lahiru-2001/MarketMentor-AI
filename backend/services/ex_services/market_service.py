from backend.api_clients.twelve_data import get_time_series
from backend.api_clients.newsapi import get_market_news
from cse_lk import CSEClient


def get_live_prices(asset_type: str, symbol: str):
    """
    Fetch live historical closing prices for both GLOBAL stocks and CSE stocks.

    Parameters:
        asset_type (str): Market type ("GLOBAL" or "CSE")
        symbol (str): Stock symbol (e.g., AAPL, JKH)

    Returns:
        list: List of closing prices
    """

    # If the asset belongs to the global market
    if asset_type == "GLOBAL":

        # Fetch time series data from Twelve Data API
        data = get_time_series(symbol)

        # Extract closing prices from API response
        prices = [
            float(row["close"])
            for row in data["values"]
        ]

        # Reverse list so oldest data comes first
        prices.reverse()

        return prices

    # If the asset belongs to Colombo Stock Exchange
    elif asset_type == "CSE":

        # Create CSE client connection
        client = CSEClient()

        # Format symbol according to CSE standard
        symbol_full = f"{symbol}.N0000"

        # Fetch historical market data
        history = client.get_history(symbol_full)

        prices = []

        # Extract closing prices from historical records
        for row in history:
            prices.append(float(row.close))

        # Return last 150 price points only
        return prices[-150:]

    # Return empty list if asset type is invalid
    return []


def get_live_news(symbol: str):
    """
    Fetch latest market news headlines related to a stock symbol.

    Parameters:
        symbol (str): Stock symbol

    Returns:
        list: List of news headlines
    """

    try:
        # Fetch news articles related to stock symbol
        news = get_market_news(symbol)

        headlines = []

        # Extract title from each news article
        for item in news:
            title = item.get("title")

            # Add title only if available
            if title:
                headlines.append(title)

        # If no headlines found, return fallback message
        if not headlines:
            return [f"No recent news found for {symbol}"]

        return headlines

    except Exception as e:
        # Print error for debugging
        print("News fetch error:", e)

        # Return fallback message if API fails
        return [f"No recent news available for {symbol}"]