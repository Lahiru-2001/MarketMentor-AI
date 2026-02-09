import requests
from utils.api_key_manager import get_next_key

def get_crypto_price(symbol="BTC"):
    for _ in range(5):
        api_key = get_next_key("COINMARKETCAP_KEYS")
        response = requests.get(
            "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest",
            headers={"X-CMC_PRO_API_KEY": api_key},
            params={"symbol": symbol}
        )

        if response.status_code == 200:
            return response.json()

    raise Exception("CoinMarketCap API limit exceeded")
