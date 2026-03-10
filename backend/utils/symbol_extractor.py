import re

def extract_symbol(query: str):
    query_upper = query.upper()

    # ---- Crypto Mapping ----
    crypto_map = {
        "BITCOIN": "BTC",
        "BTC": "BTC",
        "ETHEREUM": "ETH",
        "ETH": "ETH"
    }

    for key in crypto_map:
        if key in query_upper:
            return crypto_map[key]

    # ---- Remove currency patterns like Rs.5000 ----
    query_cleaned = re.sub(r"\bRS\.?\s?\d+[,\d]*", "", query_upper)

    matches = re.findall(r"\b[A-Z]{2,5}\b", query_cleaned)

    ignore_words = {
        "WHAT", "SHOULD", "INVEST", "SELL", "BUY",
        "MARKET", "STOCK", "SHARES", "OUTLOOK",
        "RECOMMEND", "THE", "FOR", "SRI", "LANKAN",
        "DO", "YOU", "IS", "SAFE", "PRICE",
        "IN", "AND", "OF", "TO",
        "RS", "USD", "AS", "STARTING"
    }

    for match in matches:
        if match not in ignore_words:
            return match

    return None