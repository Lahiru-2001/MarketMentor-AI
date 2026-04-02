import re   # Import regular expressions module for pattern matching

# ---------------- US STOCK SYMBOL LIST ----------------
# Contains supported major US stock market symbols
US_SYMBOLS = {
    "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA",
    "META", "NVDA", "NFLX", "AMD", "INTC",
    "ORCL", "IBM", "BABA", "UBER", "SHOP"
}

# ---------------- CSE STOCK SYMBOL LIST ----------------
# Contains supported Colombo Stock Exchange symbols
CSE_SYMBOLS = {
    "JKH", "LOLC", "COMB", "SAMP", "HNB",
    "DIAL", "SLT", "EXPO"
}


# ======================================================
# FUNCTION: route_query
# Purpose:
# Detect user query type and decide:
# - Which market the symbol belongs to
# - Whether user requests prediction or normal analysis
# ======================================================
def route_query(user_query: str) -> dict:

    # Convert entire query to uppercase
    # This ensures case-insensitive symbol detection
    query = user_query.upper()

    # ---------------- SYMBOL DETECTION ----------------
    # Regex searches for stock symbols:
    # \b = word boundary
    # [A-Z]{2,5} = 2 to 5 uppercase letters
    match = re.search(r"\b[A-Z]{2,5}\b", query)

    symbol = None

    # If symbol found, extract first matching symbol
    if match:
        symbol = match.group()

    # ---------------- PRICE PREDICTION INTENT ----------------
    # Keywords that indicate user wants future price prediction
    prediction_keywords = [
        "CLOSE PRICE",
        "TODAY PRICE",
        "PREDICT PRICE",
        "FORECAST PRICE",
        "WHAT WILL BE",
        "TODAY CLOSE"
    ]

    # Check:
    # 1. Symbol exists
    # 2. Query contains prediction-related keywords
    if symbol and any(word in query for word in prediction_keywords):

        # If symbol belongs to US market
        if symbol in US_SYMBOLS:
            return {
                "asset_type": "GLOBAL",          # US/global stock
                "intent": "PRICE_PREDICTION",    # Prediction request
                "symbol": symbol
            }

        # If symbol belongs to Colombo Stock Exchange
        if symbol in CSE_SYMBOLS:
            return {
                "asset_type": "CSE",             # Sri Lankan stock
                "intent": "PRICE_PREDICTION",    # Prediction request
                "symbol": symbol
            }

    # ---------------- NORMAL ANALYSIS ----------------
    # If symbol exists but no prediction keyword found
    if symbol:

        # US market normal analysis
        if symbol in US_SYMBOLS:
            return {
                "asset_type": "GLOBAL",
                "intent": "ASSET_ANALYSIS",
                "symbol": symbol
            }

        # Colombo market normal analysis
        if symbol in CSE_SYMBOLS:
            return {
                "asset_type": "CSE",
                "intent": "ASSET_ANALYSIS",
                "symbol": symbol
            }

    # ---------------- GENERAL QUERY ----------------
    # If no known symbol found, treat as general financial advice query
    return {
        "asset_type": "GENERAL",
        "intent": "GENERAL_ADVICE"
    }