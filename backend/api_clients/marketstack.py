import requests
import os
from utils.env_loader import load_dotenv

API_KEY = os.getenv("MARKETSTACK_KEY")

def get_market_data(symbol):
    url = "http://api.marketstack.com/v1/eod"
    params = {
        "access_key": API_KEY,
        "symbols": symbol
    }
    return requests.get(url, params=params).json()
