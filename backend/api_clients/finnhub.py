import requests
from utils.api_key_manager import get_next_key

def get_stock_quote(symbol):
    for _ in range(5):
        api_key = get_next_key("FINNHUB_KEYS")
        response = requests.get(
            "https://finnhub.io/api/v1/quote",
            params={"symbol": symbol, "token": api_key}
        )

        if response.status_code == 200:
            return response.json()

    raise Exception("Finnhub rate limit exceeded")
