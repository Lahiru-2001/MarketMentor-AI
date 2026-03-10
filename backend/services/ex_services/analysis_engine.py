import re
from backend.services.ex_services.recommendation_engine import generate_recommendation
from backend.services.ex_services.explanation_engine import generate_personalized_explanation


def extract_investment_amount(question: str):
    """
    Extract investment amount from user question (Rs. 5,000 / 5000 etc.)
    """
    match = re.search(r"(?:rs\.?|lkr)?\s?([\d,]+)", question.lower())
    if match:
        amount = match.group(1).replace(",", "")
        return float(amount)
    return None


def analyze_asset(
    prices: list,
    news_texts: list,
    user_risk: str,
    asset_type: str,
    symbol: str,
    user_question: str
) -> str:
    """
    Main AI Brain — Now question-aware & personalized
    """

    ai_output = generate_recommendation(
        prices=prices,
        news_text=news_texts,
        user_risk=user_risk
    )

    investment_amount = extract_investment_amount(user_question)

    current_price = prices[-1]

    shares = None
    if investment_amount:
        shares = int(investment_amount // current_price)

    final_answer = generate_personalized_explanation(
        ai_output=ai_output,
        asset_type=asset_type,
        symbol=symbol,
        user_risk=user_risk,
        user_question=user_question,
        investment_amount=investment_amount,
        shares=shares,
        current_price=current_price
    )

    return final_answer
