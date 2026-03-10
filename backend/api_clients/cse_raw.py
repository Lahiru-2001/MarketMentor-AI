import requests

BASE_URL = "https://www.cse.lk/api"

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "MarketMentor-AI/1.0"
}


def get_today_share_prices() -> list:
    """
    Fetch today's share prices from CSE
    """
    url = f"{BASE_URL}/todaySharePrice"

    try:
        # Use POST as CSE sometimes blocks GET
        response = requests.post(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}. Trying fallback...")
        return []  # Return empty list if API fails
    except requests.exceptions.RequestException as e:
        print(f" Request Exception: {e}. Returning empty list.")
        return []