# Import Groq client object and availability flag from API client module
from backend.api_clients.groq_client import client, GROQ_AVAILABLE


# Main function to generate investment strategy response
def generate_strategy_response(question: str):

    # If Groq API is unavailable or client failed to initialize,
    # use fallback static strategy generator
    if not GROQ_AVAILABLE or client is None:
        return _fallback_strategy(question)

    # Build AI prompt with professional financial advisor instructions
    prompt = f"""
You are a professional Sri Lankan investment advisor.

Answer clearly and professionally.

Rules:
- Provide structured advice
- Maximum 250 words
- Practical guidance
- If money mentioned, suggest allocation plan

Question:
{question}
"""

    try:
        # Send request to Groq AI model
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",   # Selected Groq model
            messages=[
                {"role": "system", "content": "You are a disciplined financial advisor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,   # Low randomness for stable financial advice
            max_tokens=350      # Limit response length
        )

        # Return generated response text
        return response.choices[0].message.content.strip()

    except Exception as e:
        # If API call fails, print error and return fallback strategy
        print("Groq strategy error:", e)
        return _fallback_strategy(question)


# Backup response generator when AI is unavailable
def _fallback_strategy(question):

    # Predefined stable Sri Lankan stock list
    stocks = [
        "John Keells Holdings (JKH)",
        "Ceylon Tobacco Company (CTC)",
        "Distilleries Company of Sri Lanka (DCSL)",
        "Commercial Bank of Ceylon (COMB)",
        "Sampath Bank (SAMPATH)"
    ]

    # Suggested simple portfolio allocation
    allocation = [
        "40% to JKH or CTC for long-term growth",
        "30% to DCSL or COMB for income generation",
        "30% to SAMPATH for a balanced portfolio"
    ]

    # Convert stock list into numbered display format
    stock_list = "\n".join([f"{i+1}. {s}" for i, s in enumerate(stocks)])

    # Convert allocation list into bullet format
    allocation_list = "\n".join([f"* {a}" for a in allocation])

    # Return formatted fallback guidance message
    return f"""
General Investment Guidance:

As a Sri Lankan investment advisor, I recommend considering the following low-risk stocks for a diversified portfolio:

{stock_list}

Suggested Allocation:

{allocation_list}

This is educational guidance only.
"""