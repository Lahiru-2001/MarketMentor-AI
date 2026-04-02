import numpy as np  # Import numpy for numerical operations (not strictly used here but useful for extensions)

def explain_recommendation(features):
    """
    Generate a lightweight, SHAP-style explanation for a recommendation.
    This function approximates feature impacts without requiring the SHAP library.
    
    Parameters:
        features (list or array-like): List containing feature values:
            - features[0]: Sentiment score
            - features[1]: Forecast impact score
            
    Returns:
        dict: Dictionary with rounded impact values for each feature.
              Keys: "Sentiment Impact", "Forecast Impact"
    """
    
    # Extract individual feature values
    sentiment = features[0]
    forecast_impact = features[1]

    # Build explanation dictionary with rounded feature impacts
    explanation = {
        "Sentiment Impact": round(float(sentiment), 4),  # Rounded to 4 decimal places for readability
        "Forecast Impact": round(float(forecast_impact), 4)
    }

    # Return the explanation dictionary
    return explanation