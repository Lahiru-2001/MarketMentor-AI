def format_explanation(ai_output, shap_values):
    explanation = f"""
    Recommendation: {ai_output['recommendation']}
    Trend: {ai_output['predicted_trend']}
    Confidence: {ai_output['confidence']}

    Key Factors:
    """
    for k, v in shap_values.items():
        explanation += f"- {k}: impact {round(v, 3)}\n"

    return explanation
