import requests
from utils.api_key_manager import get_next_key

def get_market_data(symbol):
    for _ in range(4):
        api_key = get_next_key("MARKETSTACK_KEYS")
        response = requests.get(
            "http://api.marketstack.com/v1/eod",
            params={"access_key": api_key, "symbols": symbol}
        )

        if response.status_code == 200:
            return response.json()

    raise Exception("Marketstack API limit exceeded")
