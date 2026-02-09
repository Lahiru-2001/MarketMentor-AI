import requests
from utils.api_key_manager import get_next_key

def get_financial_news(query="investment"):
    for _ in range(4):
        api_key = get_next_key("NEWS_API_KEYS")
        response = requests.get(
            "https://newsapi.org/v2/everything",
            params={
                "q": query,
                "language": "en",
                "apiKey": api_key
            }
        )

        data = response.json()
        if data.get("status") == "ok":
            return data

    raise Exception("NewsAPI rate limit exceeded")
