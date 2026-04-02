def format_explanation(ai_output, shap_values):
    """
    Format AI model output and SHAP values into a human-readable explanation.
    
    Parameters:
        ai_output (dict): Dictionary containing the AI model's output, expected keys:
            - 'recommendation': Suggested action or decision.
            - 'predicted_trend': Model's prediction of trend (e.g., up, down, stable).
            - 'confidence': Confidence score of the prediction.
        shap_values (dict): Dictionary of feature names and their SHAP values indicating
                            each feature's impact on the prediction.
                            
    Returns:
        str: A formatted string summarizing the AI recommendation, trend, confidence,
             and key factors with their impact values.
    """

    # Start building the explanation string with recommendation, trend, and confidence
    explanation = f"""
    Recommendation: {ai_output['recommendation']}
    Trend: {ai_output['predicted_trend']}
    Confidence: {ai_output['confidence']}

    Key Factors:
    """

    # Add each feature's impact from SHAP values to the explanation
    for k, v in shap_values.items():
        # Round the impact to 3 decimal places for readability
        explanation += f"- {k}: impact {round(v, 3)}\n"

    # Return the fully formatted explanation
    return explanation