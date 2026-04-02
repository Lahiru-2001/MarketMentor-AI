# Words that indicate positive sentiment
positive_words = [
    "growth", "profit", "bullish", "increase", "positive",
    "recovery", "strong", "gain", "improvement"
]

# Words that indicate negative sentiment
negative_words = [
    "loss", "decline", "bearish", "drop",
    "crisis", "weak", "fall", "risk"
]

# SENTIMENT ANALYSIS FUNCTION
def analyze_sentiment(texts: list) -> float:
    """
    Perform a simple rule-based sentiment analysis on a list of texts.

    Parameters:
    -----------
    texts : list
        List of strings (e.g., news headlines, tweets, or articles)

    Returns:
    --------
    float
        Sentiment score normalized between 0 and 1:
        - 0 = very negative
        - 0.5 = neutral
        - 1 = very positive

    Method:
    -------
    - Iterate through each text in the input list
    - Convert text to lowercase for case-insensitive matching
    - For each positive word present, add +1 to the score
    - For each negative word present, subtract -1 from the score
    - Normalize the score to the range [0,1]
    """

    score = 0  # cumulative sentiment score
    total = 0  # number of texts processed

    for text in texts:
        text = text.lower()  # make matching case-insensitive

        # Count positive words
        for word in positive_words:
            if word in text:
                score += 1

        # Count negative words
        for word in negative_words:
            if word in text:
                score -= 1

        total += 1  # increment count of texts processed

    # If no texts are provided, return neutral sentiment
    if total == 0:
        return 0.5

    # Normalize score:
    normalized = (score / (total * 5)) + 0.5

    # Clamp to [0,1] to avoid overflow
    return max(0, min(normalized, 1))