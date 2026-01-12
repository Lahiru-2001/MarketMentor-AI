import requests
import os
from utils.env_loader import load_dotenv

API_KEY = os.getenv("TWELVE_DATA_KEY")

def get_time_series(symbol):
    url = "https://api.twelvedata.com/time_series"
    params = {
        "symbol": symbol,
        "interval": "1day",
        "apikey": API_KEY
    }
    return requests.get(url, params=params).json()
