import requests
import os
from utils.env_loader import load_dotenv

API_KEY = os.getenv("FINNHUB_KEY")

def get_stock_quote(symbol):
    url = "https://finnhub.io/api/v1/quote"
    params = {"symbol": symbol, "token": API_KEY}
    return requests.get(url, params=params).json()
