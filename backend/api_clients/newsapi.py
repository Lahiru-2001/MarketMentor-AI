import requests
from backend.utils.api_key_manager import get_next_key


def get_market_news(symbol: str):

    api_key = get_next_key("NEWS_API_KEYS")

    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={symbol}&"
        f"sortBy=publishedAt&"
        f"language=en&"
        f"apiKey={api_key}"
    )

    response = requests.get(url)

    data = response.json()

    return data.get("articles", [])