from sqlalchemy import text

def save_recommendation(db, data):
    query = text("""
        INSERT INTO recommendation_history
        (user_id, question, asset_type, symbol, recommendation,
         confidence, predicted_trend, explanation)
        VALUES (:user_id, :question, :asset_type, :symbol,
                :recommendation, :confidence,
                :predicted_trend, :explanation)
    """)

    db.execute(query, data)
    db.commit()


def save_support_message(db, data):
    query = text("""
        INSERT INTO support
        (user_id, username, email, issue_type, description, status)
        VALUES (:user_id, :username, :email,
                :issue_type, :description, :status)
    """)

    db.execute(query, data)
    db.commit()