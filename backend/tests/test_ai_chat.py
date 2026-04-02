import sys
from pathlib import Path
import re


sys.path.append(str(Path(__file__).resolve().parents[1]))

from api_clients.coinmarketcap import get_crypto_price
from api_clients.newsapi import get_financial_news
from services.ex_services.analysis_engine import analyze_asset
from backend.services.ex_services.query_router import route_query
from backend.services.ex_services.strategy_engine import generate_strategy_response


from cse_lk import CSEClient
cse_client = CSEClient()



def get_live_prices(asset_type, symbol, days=30):
    try:

        # ------------------ CRYPTO ------------------
        if asset_type == "CRYPTO":
            data = get_crypto_price(symbol)

            if not data or "data" not in data:
                raise Exception("Invalid crypto API response")

            price = data["data"][symbol]["quote"]["USD"]["price"]
            return [float(price)] * days

        # ------------------ CSE ------------------
        elif asset_type == "CSE":
            symbol_full = f"{symbol}.N0000"
            try:
                company = cse_client.get_company_info(symbol_full)
                price = company.last_traded_price
                return [float(price)] * days
            except Exception as e:
                print(f"CSE fetch error for {symbol}: {e}")
                return None

        else:
            raise ValueError("Unsupported asset type")

    except Exception as e:
        print("Live price fetch error:", e)
        return None



def get_live_news(symbol):
    try:
        news = get_financial_news(symbol)
        articles = news.get("articles", [])
        return [a["title"] for a in articles[:10]]
    except Exception:
        return []



def extract_symbol(query):
    query_upper = query.upper()

    # ---- Crypto Mapping ----
    crypto_map = {
        "BITCOIN": "BTC",
        "BTC": "BTC",
        "ETHEREUM": "ETH",
        "ETH": "ETH"
    }

    for key in crypto_map:
        if key in query_upper:
            return crypto_map[key]

    # ---- Remove currency patterns like Rs.5000 ----
    query_cleaned = re.sub(r"\bRS\.?\s?\d+[,\d]*", "", query_upper)

    matches = re.findall(r"\b[A-Z]{2,5}\b", query_cleaned)

    ignore_words = {
        "WHAT", "SHOULD", "INVEST", "SELL", "BUY",
        "MARKET", "STOCK", "SHARES", "OUTLOOK",
        "RECOMMEND", "THE", "FOR", "SRI", "LANKAN",
        "DO", "YOU", "IS", "SAFE", "PRICE",
        "IN", "AND", "OF", "TO",
        "RS", "USD", "AS", "STARTING"
    }

    for match in matches:
        if match not in ignore_words:
            return match

    return None



if __name__ == "__main__":

    print("===============================================")
    print("        MARKETMENTOR AI TEST CONSOLE")
    print("===============================================")

    while True:
        user_query = input("\n-- Ask your investment question (or type exit): ")

        if user_query.lower() == "exit":
            break

 
        route = route_query(user_query)
        asset_type = route.get("asset_type")
        intent = route.get("intent")

    
        if intent in ["INVESTMENT_STRATEGY", "GENERAL_ADVICE", "MACRO_ANALYSIS"]:

            print("\n===============================================")
            print("        STRATEGY / ADVISORY RESPONSE")
            print("===============================================\n")

            answer = generate_strategy_response(user_query)
            print(answer)
            continue

     
        if intent == "ASSET_ANALYSIS":

            symbol = extract_symbol(user_query)

            if not symbol:
                print("=== Could not detect asset symbol. ===")
                continue

            print(f"\n-- Detected Asset Type: {asset_type}")
            print(f"-- Detected Symbol: {symbol}")

            prices = get_live_prices(asset_type, symbol)

            if not prices:
                print("=== Could not fetch live prices. ===")
                continue

            news = get_live_news(symbol)

          
            answer = analyze_asset(
                prices=prices,
                news_texts=news,
                user_risk="Medium",
                asset_type=asset_type,
                symbol=symbol,
                user_question=user_query
            )

            print("\n===============================================")
            print("        PERSONALIZED INVESTMENT ADVICE")
            print("===============================================\n")
            print(answer)
            continue

    
        if intent in ["TECHNICAL_ANALYSIS", "FUNDAMENTAL_ANALYSIS"]:
            print("\n This analysis type is detected but not yet implemented.")
            continue

    
        print("\nUnable to determine proper intent.")
        print("Try asking about a specific stock symbol or investment strategy.")
