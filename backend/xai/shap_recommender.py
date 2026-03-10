import numpy as np

def explain_recommendation(features):
    """
    Lightweight explanation engine (SHAP-style approximation)
    No external SHAP dependency required
    """

    sentiment = features[0]
    forecast_impact = features[1]

    explanation = {
        "Sentiment Impact": round(float(sentiment), 4),
        "Forecast Impact": round(float(forecast_impact), 4)
    }

    return explanation
