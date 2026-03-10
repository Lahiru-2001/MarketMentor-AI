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
    Generates question-aware professional investment answer.
    """

    if not GROQ_AVAILABLE:
        return _fallback_answer(symbol, investment_amount, shares, current_price)

    recommendation = ai_output.get("recommendation")
    trend = ai_output.get("predicted_trend")
    confidence = ai_output.get("confidence")
    sentiment = ai_output.get("sentiment")
    risk = ai_output.get("risk")
    forecast = ai_output.get("forecast_price")

    prompt = f"""
You are a professional Sri Lankan investment advisor.

A user asked:
"{user_question}"

Current Market Data:
Symbol: {symbol}
Current Price: Rs. {current_price}
Forecast Price: {forecast}
Market Trend: {trend}
Sentiment Score: {sentiment}
Risk Level: {risk}
AI Recommendation: {recommendation}
Confidence: {confidence}

If investment amount is provided:
Investment Amount: {investment_amount}
Estimated Shares: {shares}

Generate a professional structured answer:

1. Directly answer the user's question first.
2. If amount provided, calculate and mention share count.
3. Provide 2026 investment insights.
4. Mention valuation, growth, dividends (if relevant).
5. Provide beginner considerations.
6. Keep it professional and structured.
7. Max 400 words.
8. No repetition.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a disciplined financial advisor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=600
    )

    return response.choices[0].message.content.strip()


def _fallback_answer(symbol, investment_amount, shares, current_price):

    if investment_amount and shares:
        return f"""
Investing Rs. {investment_amount:,.0f} in {symbol} at the current price of Rs. {current_price}
allows you to purchase approximately {shares} shares.

This can be a reasonable starting investment, especially for learning purposes.
However, consider diversification, transaction costs, and long-term strategy.

This is educational analysis only.
""".strip()

    return f"""
{symbol} appears suitable for long-term investment depending on risk profile.
Please consider diversification and market conditions.

This is educational analysis only.
""".strip()
