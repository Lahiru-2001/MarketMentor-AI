import requests
import os
from utils.env_loader import load_dotenv

API_KEY = os.getenv("EODHD_KEY")

def get_eod_data(symbol):
    url = f"https://eodhd.com/api/eod/{symbol}"
    params = {
        "api_token": API_KEY,
        "fmt": "json"
    }
    return requests.get(url, params=params).json()
