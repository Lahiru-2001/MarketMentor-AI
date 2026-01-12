import requests
import os
from utils.env_loader import load_dotenv

API_KEY = os.getenv("ALPHA_VANTAGE_KEY")

def get_company_overview(symbol):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "OVERVIEW",
        "symbol": symbol,
        "apikey": API_KEY
    }
    return requests.get(url, params=params).json()
