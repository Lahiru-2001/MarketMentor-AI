import sys
from pathlib import Path

# Add backend directory to PYTHONPATH
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

from api_clients.alpha_vantage import get_company_overview
from api_clients.finnhub import get_stock_quote
from api_clients.eodhd import get_eod_data
from api_clients.marketstack import get_market_data
from api_clients.twelve_data import get_time_series
from api_clients.coinmarketcap import get_crypto_price
from api_clients.newsapi import get_financial_news


def run_test(name, func):
    try:
        func()
        print(f"- {name}: OK")
    except Exception as e:
        print(f"- {name}: FAILED → {e}")

if __name__ == "__main__":
    print("\n🔍 API KEY HEALTH CHECK\n")

    run_test("Alpha Vantage", lambda: get_company_overview("AAPL"))
    run_test("Finnhub", lambda: get_stock_quote("AAPL"))
    run_test("EODHD", lambda: get_eod_data("AAPL.US"))
    run_test("MarketStack", lambda: get_market_data("AAPL"))
    run_test("Twelve Data", lambda: get_time_series("AAPL"))
    run_test("CoinMarketCap", lambda: get_crypto_price("BTC"))
    run_test("NewsAPI", lambda: get_financial_news("stocks"))

    print("\n===API key check completed===\n")
