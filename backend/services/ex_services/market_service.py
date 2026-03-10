from backend.api_clients.coinmarketcap import get_crypto_price
from backend.api_clients.newsapi import get_financial_news
from cse_lk import CSEClient


def get_live_prices(asset_type: str, symbol: str):

    if asset_type == "CRYPTO":
        data = get_crypto_price(symbol)
        price = data["data"][symbol]["quote"]["USD"]["price"]
        return [float(price)] * 30

    elif asset_type == "CSE":
        try:
            client = CSEClient()
            symbol_full = f"{symbol}.N0000"
            company = client.get_company_info(symbol_full)
            price = company.last_traded_price
            return [float(price)] * 30
        except Exception as e:
            print("CSE fetch error:", e)
            return None

    return None


def get_live_news(symbol: str):
    try:
        return get_financial_news(symbol)
    except Exception as e:
        return {"error": f"News fetch error: {str(e)}"}