import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

from api_clients.alpha_vantage import get_company_overview
from api_clients.finnhub import get_stock_quote
from api_clients.eodhd import get_eod_data
from api_clients.marketstack import get_market_data
from api_clients.twelve_data import get_time_series
from api_clients.coinmarketcap import get_crypto_price
from api_clients.newsapi import get_financial_news

from api_clients.google_api_key import client, GEMINI_AVAILABLE


def run_test(name, func):
    try:
        func()
        print(f"- {name}: OK")
    except Exception as e:
        print(f"- {name}: FAILED → {e}")



def get_valid_text_model():
    if not GEMINI_AVAILABLE:
        raise Exception("Gemini not configured or API key missing")

    models = client.models.list()
    for m in models:
     
        if hasattr(m, "name") and hasattr(m, "capabilities"):
            caps = [c.name.lower() for c in m.capabilities]
            if "generatecontent" in caps:
                return m.name
    raise Exception("No model supporting text generation found")


def test_gemini():
    model_name = get_valid_text_model()
    print(f"→ Using Gemini model: {model_name}")

    response = client.models.generate_content(
        model=model_name,
        contents="Say 'Gemini API is working' in one short sentence."
    )

    if not response or not response.text:
        raise Exception("Empty response from Gemini")


if __name__ == "__main__":
    print("\n API KEY HEALTH CHECK\n")

    run_test("Alpha Vantage", lambda: get_company_overview("AAPL"))
    run_test("Finnhub", lambda: get_stock_quote("AAPL"))
    run_test("EODHD", lambda: get_eod_data("AAPL.US"))
    run_test("MarketStack", lambda: get_market_data("AAPL"))
    run_test("Twelve Data", lambda: get_time_series("AAPL"))
    run_test("CoinMarketCap", lambda: get_crypto_price("BTC"))
    run_test("NewsAPI", lambda: get_financial_news("stocks"))

    run_test("Google Gemini", test_gemini)

    print("\n=== API key check completed ===\n")
