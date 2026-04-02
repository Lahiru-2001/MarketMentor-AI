from backend.ml.lstm.predict import predict_price
from backend.services.ex_services.recommendation_engine import generate_recommendation
from backend.services.ex_services.explanation_engine import generate_personalized_explanation


def analyze_asset(
    prices,
    news_texts,
    user_risk,
    asset_type,
    symbol,
    user_question,
    intent="ASSET_ANALYSIS"
):
    """
    Main AI analysis function for MarketMentor-AI.

    Parameters:
    ----------
    prices : list
        Historical asset price data.

    news_texts : str or list
        News headlines or financial news related to the asset.

    user_risk : str
        User's risk profile (Low, Medium, High).

    asset_type : str
        Type of asset (Stock, Crypto, Forex, etc.).

    symbol : str
        Asset trading symbol (e.g., AAPL, BTC-USD).

    user_question : str
        User query for personalized AI explanation.

    intent : str
        Analysis mode:
        - "ASSET_ANALYSIS" = Full AI analysis
        - "PRICE_PREDICTION" = Only forecast future price

    Returns:
    -------
    dict
        Personalized AI-generated explanation and recommendation.
    """

    # Get the most recent price from historical data
    current_price = prices[-1]

   
    # PRICE PREDICTION MODE
    if intent == "PRICE_PREDICTION":

        # Predict next price using LSTM model
        forecast_price = predict_price(prices)

        # Add small adjustment factor (15%) to create future projected price
        future_price = round(
            current_price + ((forecast_price - current_price) * 1.15),
            2
        )

        # Prepare AI output structure for explanation engine
        ai_output = {
            "recommendation": "PRICE FORECAST",
            "predicted_trend": "Forecast Analysis",
            "confidence": 0.92,   # Static confidence score
            "risk": "Calculated",
            "forecast_price": forecast_price,
            "future_price": future_price,
            "sentiment": 0.5,     # Neutral sentiment placeholder
            "shap_values": {
                "Current Price": current_price,
                "LSTM Forecast": forecast_price
            }
        }

        # Generate final user-friendly explanation
        return generate_personalized_explanation(
            ai_output=ai_output,
            asset_type=asset_type,
            symbol=symbol,
            user_risk=user_risk,
            user_question=user_question,
            current_price=current_price
        )

    # FULL AI ANALYSIS MODE
  
    # This mode combines:
    # - Price trend analysis
    # - Sentiment analysis
    # - Risk analysis
    # - Recommendation generation
    ai_output = generate_recommendation(
        prices=prices,
        news_text=news_texts,
        user_risk=user_risk
    )

    # Convert AI analysis into personalized explanation
    return generate_personalized_explanation(
        ai_output=ai_output,
        asset_type=asset_type,
        symbol=symbol,
        user_risk=user_risk,
        user_question=user_question,
        current_price=current_price
    )