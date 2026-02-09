import requests
from utils.api_key_manager import get_next_key

def get_time_series(symbol):
    for _ in range(5):
        api_key = get_next_key("TWELVE_DATA_KEYS")
        response = requests.get(
            "https://api.twelvedata.com/time_series",
            params={
                "symbol": symbol,
                "interval": "1day",
                "apikey": api_key
            }
        )

        data = response.json()
        if "code" not in data:
            return data

    raise Exception("Twelve Data rate limit exceeded")
