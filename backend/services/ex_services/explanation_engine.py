from backend.api_clients.groq_client import client, GROQ_AVAILABLE


def generate_personalized_explanation(
    ai_output,
    asset_type,
    symbol,
    user_risk,
    user_question,
    investment_amount=None,
    shares=None,
    current_price=None
):
    """
    Generate a full professional investment analysis report.

    Parameters:
    ----------
    ai_output : dict
        AI prediction results including recommendation, forecast, sentiment, etc.

    asset_type : str
        Type of asset (stock, crypto, forex, etc.)

    symbol : str
        Investment symbol (example: AAPL, TSLA)

    user_risk : str
        User risk preference (low / medium / high)

    user_question : str
        User's original investment question

    investment_amount : float, optional
        Amount user plans to invest

    shares : int, optional
        Number of shares user wants to buy

    current_price : float, optional
        Current market price

    Returns:
    -------
    str
        Full formatted AI investment report
    """

    # Extract prediction values from AI output dictionary
    recommendation = ai_output.get("recommendation")
    trend = ai_output.get("predicted_trend")
    confidence = ai_output.get("confidence")
    sentiment = ai_output.get("sentiment")
    risk = ai_output.get("risk")
    forecast = ai_output.get("forecast_price")
    future_price = ai_output.get("future_price")
    shap_values = ai_output.get("shap_values", {})

    # Convert sentiment score into percentage
    sentiment_percent = round(sentiment * 100, 1)

    # Convert confidence score into readable label
    confidence_label = (
        "High" if confidence > 0.7 else
        "Moderate" if confidence > 0.4 else
        "Low"
    )

    # ================= AI EXPLANATION SECTION =================
    explanation = ""

    # Use Groq AI if available
    if GROQ_AVAILABLE:

        # Prompt sent to AI model
        prompt = f"""
You are a professional Sri Lankan investment advisor.

User asked:
{user_question}

Symbol: {symbol}
Current Price: {current_price}
Forecast Price: {forecast}
Future Price: {future_price}
Recommendation: {recommendation}
Risk: {risk}

Provide concise investment explanation.
"""

        try:
            # Request explanation from Groq LLM
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are a disciplined financial advisor."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=400
            )

            # Extract AI response text
            explanation = response.choices[0].message.content.strip()

        except:
            # Fallback explanation if Groq fails
            explanation = _fallback_explanation(symbol, forecast)

    else:
        # Fallback explanation if Groq unavailable
        explanation = _fallback_explanation(symbol, forecast)

    # ================= FINAL FORMATTED OUTPUT =================
    output = f"""
 AI INVESTMENT ANALYSIS


== Recommendation :- {recommendation}
== Market Trend   :- {trend}
== Confidence     :- {confidence_label} ({confidence * 100:.0f}%)
== Risk Level     :- {risk}
== Future Price   :- {future_price}
== Forecast Price :- {forecast:,.2f}
== Market Sentiment :- {sentiment_percent}%


 Key Influencing Factors

"""

    # Add SHAP feature importance values
    for key, value in shap_values.items():
        output += f"• {key}: {round(value, 4)}\n"

    # Append explanation and disclaimer section
    output += f"""


 AI Explanation 

{explanation}


 Investment Disclaimer 

-- This is AI-generated analysis with financial advice.
-- Markets are volatile. Always do your own research.
(IMPORTANT: This is financial advice. Always consult a financial advisor before making investment decisions.)
== AI predictions are based on historical data and current trends, but they cannot guarantee future performance. Use this information as one of many tools in your investment decision-making process.==

"""

    # Return final formatted string
    return output.strip()


def _fallback_explanation(symbol, forecast):
    """
    Fallback explanation when AI model is unavailable.

    Parameters:
    ----------
    symbol : str
        Asset symbol

    forecast : float
        Forecasted price

    Returns:
    -------
    str
        Basic explanation text
    """
    return f"""
{symbol} shows current market movement toward Rs. {forecast:,.2f}.
The recommendation is based on price trend, sentiment, and volatility analysis.
Diversification is recommended before making investment decisions.
""".strip()