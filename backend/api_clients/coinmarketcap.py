import requests
import os
from utils.env_loader import load_dotenv

API_KEY = os.getenv("COINMARKETCAP_KEY")

def get_crypto_price(symbol="BTC"):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {
        "X-CMC_PRO_API_KEY": API_KEY
    }
    params = {
        "symbol": symbol
    }
    return requests.get(url, headers=headers, params=params).json()
