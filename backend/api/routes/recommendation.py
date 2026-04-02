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

# Create API router instance
router = APIRouter()

# Request Model for /ask endpoint
class QuestionRequest(BaseModel):
    question: str

# Request Model for /save endpoint
class SaveRecommendationRequest(BaseModel):
    question: str
    asset_type: str
    symbol: str | None
    recommendation: str
    confidence: float
    predicted_trend: str
    explanation: str


# Extract current user ID from JWT token
def get_current_user_id(token: str):
    try:
        # Decode JWT token using secret key and algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Return user ID stored in "sub" field
        return int(payload.get("sub"))

    except JWTError:
        # Return None if token is invalid
        return None


# AI Question Processing Endpoint
@router.post("/ask")
def ask_ai(
    request: QuestionRequest,
    db: Session = Depends(get_db),
    authorization: str = Header(None)
):
    # Check token exists
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")

    # Remove "Bearer " prefix from token
    token = authorization.replace("Bearer ", "")

    # Decode token and get user ID
    user_id = get_current_user_id(token)

    # Reject invalid token
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Get user question
    user_query = request.question

    # Route question to identify intent and asset type
    route = route_query(user_query)

    asset_type = route.get("asset_type")
    intent = route.get("intent")


    # Strategy / Advice / Macro Analysis Queries
    if intent in ["INVESTMENT_STRATEGY", "GENERAL_ADVICE", "MACRO_ANALYSIS"]:

        # Generate AI strategy response
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


    # Asset Analysis Queries
    if intent == "ASSET_ANALYSIS":

        # Extract market symbol from user question
        symbol = extract_symbol(user_query)

        # Reject if symbol not found
        if not symbol:
            raise HTTPException(status_code=400, detail="Symbol not detected")

        # Get live market prices
        prices = get_live_prices(asset_type, symbol)

        # Get latest news for symbol
        news = get_live_news(symbol)

        # Generate recommendation from AI engine
        ai_result = generate_recommendation(
            prices=prices,
            news_text=news,
            user_risk="Medium"
        )

        # Generate detailed explanation
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


# Save Recommendation Endpoint
@router.post("/save")
def save_ai_recommendation(
    request: SaveRecommendationRequest,
    db: Session = Depends(get_db),
    authorization: str = Header(None)
):
    # Validate token exists
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")

    token = authorization.replace("Bearer ", "")
    user_id = get_current_user_id(token)

    # Validate token
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Save recommendation into database
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


# Fetch User Recommendation History
@router.get("/history")
def get_user_history(
    db: Session = Depends(get_db),
    authorization: str = Header(None)
):
    # Validate token exists
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")

    token = authorization.replace("Bearer ", "")
    user_id = get_current_user_id(token)

    # Validate token
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Execute SQL query to fetch recommendation history
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

    # Fetch all rows
    rows = result.fetchall()

    # Convert rows into JSON response
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