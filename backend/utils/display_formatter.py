def format_ai_output(result: dict) -> str:
    recommendation = result.get("recommendation")
    trend = result.get("predicted_trend")
    confidence = result.get("confidence", 0)
    risk = result.get("risk")
    forecast = result.get("forecast_price")
    sentiment = result.get("sentiment")
    shap_values = result.get("shap_values", {})

    sentiment_percent = round(sentiment * 100, 1)

    confidence_label = (
        "High" if confidence > 0.7 else
        "Moderate" if confidence > 0.4 else
        "Low"
    )

    output = f"""
================ AI INVESTMENT ANALYSIS ================
========================================================

== Recommendation :- {recommendation}
== Market Trend   :- {trend}
== Confidence     :- {confidence_label} ({confidence * 100:.0f}%)
== Risk Level     :- {risk}

== Forecast Price :- {forecast:,.2f}
== Market Sentiment :- {sentiment_percent}%

========================================================
              Key Influencing Factors
========================================================
"""

    for key, value in shap_values.items():
        output += f"• {key}: {round(value, 4)}\n"

    output += """
=========================================================
                  AI Explanation
=========================================================
"""

    output += result.get("explanation", "")

    output += """

=========================================================
              Investment Disclaimer
=========================================================
-- This is AI-generated analysis with financial advice.
-- Markets are volatile. Always do your own research.
(IMPORTANT: This is not financial advice. Always consult a financial advisor before making investment decisions.)
== AI predictions are based on historical data and current trends, but they cannot guarantee future performance. Use this information as one of many tools in your investment decision-making process.==
=========================================================
"""

    return output.strip()
