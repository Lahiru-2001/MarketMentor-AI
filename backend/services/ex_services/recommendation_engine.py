import numpy as np
from backend.ml.lstm.predict import predict_price
from backend.ml.sentiment.finbert import analyze_sentiment
from backend.ml.risk.risk_classifier import predict_risk
from backend.services.ex_services.market_trend_engine import analyze_market_trend
from backend.xai.shap_recommender import explain_recommendation


def generate_recommendation(prices, news_text, user_risk="Medium"):
    """
    Generate investment recommendation using:
    - Historical stock prices
    - Financial news sentiment
    - Market trend analysis
    - Risk classification
    - Explainable AI (SHAP)

    Parameters:
    prices (list): Historical stock prices
    news_text (str): Financial news article text
    user_risk (str): User risk preference (Low / Medium / High)

    Returns:
    dict: Recommendation result with prediction details
    """

    # Get latest stock price from price series
    current_price = prices[-1]

    # Predict next price using LSTM model
    forecast_price = predict_price(prices)

    # Calculate future projected price with 15% amplified movement
    future_price = round(
        current_price + ((forecast_price - current_price) * 1.15),
        2
    )

    # Detect market trend (Uptrend / Downtrend / Sideways)
    trend = analyze_market_trend(prices)

    # Analyze sentiment score from financial news
    sentiment = analyze_sentiment(news_text)

    # Predict stock risk category
    risk = predict_risk(prices)

    # Calculate percentage price change between current and forecast
    price_change = (forecast_price - current_price) / current_price

    # Calculate volatility using standard deviation of returns
    volatility = np.std(np.diff(prices) / prices[:-1])

    # Initialize recommendation scoring system
    score = 0

    # Positive contribution from expected price increase
    score += price_change * 5

    # Add sentiment score
    score += sentiment

    # Penalize high volatility
    score -= volatility * 10

    # Add trend-based score adjustment
    if trend == "Uptrend":
        score += 1
    elif trend == "Downtrend":
        score -= 1

    # Penalize risky stocks for low-risk users
    if user_risk == "Low" and risk == "High Risk":
        score -= 2

    # Final decision logic
    if score > 1:
        decision = "BUY"
    elif score < -1:
        decision = "SELL"
    else:
        decision = "HOLD"

    # Confidence score normalized between 0 and 1
    confidence = round(min(abs(score) / 3, 1), 2)

    # Generate SHAP explanation values for transparency
    shap_values = explain_recommendation([
        sentiment,
        price_change
    ])

    # Return complete recommendation result
    return {
        "recommendation": decision,
        "predicted_trend": trend,
        "confidence": confidence,
        "risk": risk,
        "forecast_price": forecast_price,
        "future_price": future_price,
        "sentiment": sentiment,
        "shap_values": shap_values
    }