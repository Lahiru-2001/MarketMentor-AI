import numpy as np


from backend.ml.lstm.predict import predict_price
from backend.ml.sentiment.finbert import analyze_sentiment
from backend.ml.risk.risk_classifier import predict_risk
from backend.services.ex_services.market_trend_engine import analyze_market_trend
from backend.xai.shap_recommender import explain_recommendation
from backend.ml.lstm.predict import predict_price
from backend.ml.sentiment.finbert import analyze_sentiment

def generate_recommendation(prices, news_text, user_risk="Medium"):

    current_price = prices[-1]
    forecast_price = predict_price(prices)
    trend = analyze_market_trend(prices)
    sentiment = analyze_sentiment(news_text)
    risk = predict_risk(prices)

    # Feature Engineering
    price_change = (forecast_price - current_price) / current_price
    volatility = np.std(np.diff(prices) / prices[:-1])

    # AI Score
    score = 0

    score += price_change * 5
    score += sentiment
    score -= volatility * 10

    if trend == "Uptrend":
        score += 1
    elif trend == "Downtrend":
        score -= 1

    # Risk adjustment
    if user_risk == "Low" and risk == "High Risk":
        score -= 2

    # Decision
    if score > 1:
        decision = "BUY"
    elif score < -1:
        decision = "SELL"
    else:
        decision = "HOLD"

    confidence = round(min(abs(score) / 3, 1), 2)

    # SHAP Explanation
    shap_values = explain_recommendation([
        sentiment,
        price_change
    ])

    return {
        "recommendation": decision,
        "predicted_trend": trend,
        "confidence": confidence,
        "risk": risk,
        "forecast_price": forecast_price,
        "sentiment": sentiment,
        "shap_values": shap_values
    }
