positive_words = [
    "growth", "profit", "bullish", "increase", "positive",
    "recovery", "strong", "gain", "improvement"
]

negative_words = [
    "loss", "decline", "bearish", "drop",
    "crisis", "weak", "fall", "risk"
]

def analyze_sentiment(texts: list) -> float:
    """
    Rule-based live sentiment scoring
    """

    score = 0
    total = 0

    for text in texts:
        text = text.lower()
        for word in positive_words:
            if word in text:
                score += 1
        for word in negative_words:
            if word in text:
                score -= 1
        total += 1

    if total == 0:
        return 0.5

    normalized = (score / (total * 5)) + 0.5
    return max(0, min(normalized, 1))
