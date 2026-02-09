import requests
from utils.api_key_manager import get_next_key

def get_eod_data(symbol):
    for _ in range(5):
        api_key = get_next_key("EODHD_KEYS")
        response = requests.get(
            f"https://eodhd.com/api/eod/{symbol}",
            params={"api_token": api_key, "fmt": "json"}
        )

        if response.status_code == 200:
            return response.json()

    raise Exception("EODHD API limit exceeded")
