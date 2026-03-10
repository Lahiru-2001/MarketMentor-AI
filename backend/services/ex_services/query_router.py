import re

def route_query(user_query: str) -> dict:
    query = user_query.lower()

    # ---------------- CRYPTO ----------------
    if any(word in query for word in ["bitcoin", "ethereum", "crypto", "btc", "eth"]):
        return {"asset_type": "CRYPTO", "intent": "ASSET_ANALYSIS"}

    # ---------------- SYMBOL DETECTION ----------------
    if re.search(r"\b[A-Z]{2,5}\b", user_query):
        return {"asset_type": "CSE", "intent": "ASSET_ANALYSIS"}
    
    

    # ---------------- TECHNICAL ANALYSIS ----------------
    if any(word in query for word in [
        "rsi", "macd", "moving average", "bollinger",
        "support", "resistance", "fibonacci",
        "chart", "breakout", "golden cross"
    ]):
        return {"asset_type": "GENERAL", "intent": "TECHNICAL_ANALYSIS"}

    # ---------------- FUNDAMENTAL ANALYSIS ----------------
    if any(word in query for word in [
        "pe ratio", "eps", "roe", "balance sheet",
        "debt", "cash flow", "dividend", "npl"
    ]):
        return {"asset_type": "GENERAL", "intent": "FUNDAMENTAL_ANALYSIS"}

    # ---------------- STRATEGY / BEGINNER ----------------
    if any(word in query for word in [
        "start investing", "diversify", "risk", "beginner",
        "portfolio", "low risk", "strategy"
    ]):
        return {"asset_type": "GENERAL", "intent": "INVESTMENT_STRATEGY"}

    # ---------------- MACRO ----------------
    if any(word in query for word in [
        "inflation", "interest rate", "recession",
        "political", "macro", "economic"
    ]):
        return {"asset_type": "GENERAL", "intent": "MACRO_ANALYSIS"}

    return {"asset_type": "GENERAL", "intent": "GENERAL_ADVICE"}
