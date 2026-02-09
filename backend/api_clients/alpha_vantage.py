import requests
from utils.api_key_manager import get_next_key

def get_company_overview(symbol):
    for _ in range(5): 
        api_key = get_next_key("ALPHA_VANTAGE_KEYS")
        response = requests.get(
            "https://www.alphavantage.co/query",
            params={
                "function": "OVERVIEW",
                "symbol": symbol,
                "apikey": api_key
            }
        )

        data = response.json()
        if "Note" not in data:
            return data

    raise Exception("Alpha Vantage rate limit exceeded for all keys")
