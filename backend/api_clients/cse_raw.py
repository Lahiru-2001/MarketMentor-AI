import requests

BASE_URL = "https://www.cse.lk/api"

# -----------------------------
# Market Summary
# -----------------------------
def get_market_summary() -> dict:
    url = f"{BASE_URL}/marketSummery"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


# -----------------------------
# Company Info by Symbol
# -----------------------------
def get_company_info(symbol: str) -> dict:
    url = f"{BASE_URL}/companyInfoSummery?symbol={symbol}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


# -----------------------------
# Today's Share Prices
# -----------------------------
def get_today_share_prices() -> list:
    url = f"{BASE_URL}/todaySharePrice"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


# -----------------------------
# Top Gainers & Losers
# -----------------------------
def get_top_gainers() -> list:
    url = f"{BASE_URL}/topGainers"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def get_top_losers() -> list:
    url = f"{BASE_URL}/topLooses"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


# -----------------------------
# Trade Summary
# -----------------------------
def get_trade_summary() -> list:
    url = f"{BASE_URL}/tradeSummary"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


# -----------------------------
# Market Status (Open/Close)
# -----------------------------
def get_market_status() -> dict:
    url = f"{BASE_URL}/marketStatus"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
