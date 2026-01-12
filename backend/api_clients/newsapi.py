import requests
import os
from utils.env_loader import load_dotenv

API_KEY = os.getenv("NEWS_API_KEY")

def get_financial_news(query="investment"):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "language": "en",
        "apiKey": API_KEY
    }
    return requests.get(url, params=params).json()
