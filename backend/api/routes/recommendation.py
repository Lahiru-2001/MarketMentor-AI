from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from sqlalchemy import text
from backend.core.security import SECRET_KEY, ALGORITHM
from backend.core.dependencies import get_db
from backend.db.crud import save_recommendation

from services.ex_services.analysis_engine import analyze_asset
from services.ex_services.recommendation_engine import generate_recommendation
from services.ex_services.query_router import route_query
from services.ex_services.strategy_engine import generate_strategy_response
from services.ex_services.market_service import get_live_prices, get_live_news
from backend.utils.symbol_extractor import extract_symbol

router = APIRouter()



class QuestionRequest(BaseModel):
    question: str


class SaveRecommendationRequest(BaseModel):
    question: str
    asset_type: str
    symbol: str | None
    recommendation: str
    confidence: float
    predicted_trend: str
    explanation: str




def get_current_user_id(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return int(payload.get("sub"))
    except JWTError:
        return None



@router.post("/ask")
def ask_ai(
    request: QuestionRequest,
    db: Session = Depends(get_db),
    authorization: str = Header(None)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")

    token = authorization.replace("Bearer ", "")
    user_id = get_current_user_id(token)

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_query = request.question
    route = route_query(user_query)

    asset_type = route.get("asset_type")
    intent = route.get("intent")

   
    if intent in ["INVESTMENT_STRATEGY", "GENERAL_ADVICE", "MACRO_ANALYSIS"]:
        answer = generate_strategy_response(user_query)

        return {
            "question": user_query,
            "asset_type": asset_type,
            "symbol": None,
            "recommendation": "STRATEGY",
            "confidence": 1,
            "predicted_trend": "N/A",
            "explanation": answer
        }

 
    if intent == "ASSET_ANALYSIS":

        symbol = extract_symbol(user_query)
        if not symbol:
            raise HTTPException(status_code=400, detail="Symbol not detected")

        prices = get_live_prices(asset_type, symbol)
        news = get_live_news(symbol)

        ai_result = generate_recommendation(
            prices=prices,
            news_text=news,
            user_risk="Medium"
        )

        explanation = analyze_asset(
            prices=prices,
            news_texts=news,
            user_risk="Medium",
            asset_type=asset_type,
            symbol=symbol,
            user_question=user_query
        )

        return {
            "question": user_query,
            "asset_type": asset_type,
            "symbol": symbol,
            "recommendation": ai_result["recommendation"],
            "confidence": ai_result["confidence"],
            "predicted_trend": ai_result["predicted_trend"],
            "explanation": explanation
        }




@router.post("/save")
def save_ai_recommendation(
    request: SaveRecommendationRequest,
    db: Session = Depends(get_db),
    authorization: str = Header(None)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")

    token = authorization.replace("Bearer ", "")
    user_id = get_current_user_id(token)

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    save_recommendation(db, {
        "user_id": user_id,
        "question": request.question,
        "asset_type": request.asset_type,
        "symbol": request.symbol,
        "recommendation": request.recommendation,
        "confidence": request.confidence,
        "predicted_trend": request.predicted_trend,
        "explanation": request.explanation
    })

    return {"message": "Recommendation saved successfully"}



@router.get("/history")
def get_user_history(
    db: Session = Depends(get_db),
    authorization: str = Header(None)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")

    token = authorization.replace("Bearer ", "")
    user_id = get_current_user_id(token)

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    result = db.execute(
        text("""
            SELECT r_id, question, asset_type, symbol,
                   recommendation, confidence,
                   predicted_trend, explanation, created_at
            FROM recommendation_history
            WHERE user_id = :user_id
            ORDER BY created_at DESC
        """),
        {"user_id": user_id}
    )

    rows = result.fetchall()

    history = []
    for row in rows:
        history.append({
            "r_id": row[0],
            "question": row[1],
            "asset_type": row[2],
            "symbol": row[3],
            "recommendation": row[4],
            "confidence": row[5],
            "predicted_trend": row[6],
            "explanation": row[7],
            "created_at": row[8]
        })

    return {"history": history}