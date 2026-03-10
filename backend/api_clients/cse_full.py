# api_clients/cse_full.py
import requests

BASE_URL = "https://www.cse.lk/api"

def get_all_cse_prices():
    """
    Fetch all today share prices from CSE API
    Returns: list of dicts [{symbol, last_trade_price}]
    """
    url = f"{BASE_URL}/todaySharePrice"
    headers = {
        "User-Agent": "Mozilla/5.0",  # Some endpoints require a user-agent
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        all_prices = []
        for item in data:
            # Ensure numeric conversion
            try:
                price = float(item.get("ltp", 0) or 0)
                symbol = item.get("symbol")
                if symbol and price > 0:
                    all_prices.append({"symbol": symbol, "last_trade_price": price})
            except:
                continue

        if not all_prices:
            raise Exception("No valid share prices found")

        return all_prices

    except Exception as e:
        print("⚠ Error fetching all CSE prices:", e)
        return []