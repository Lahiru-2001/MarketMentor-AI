from backend.api_clients.groq_client import client, GROQ_AVAILABLE


def generate_strategy_response(question: str):

    # If Groq not initialized → fallback
    if not GROQ_AVAILABLE or client is None:
        return _fallback_strategy(question)

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
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a disciplined financial advisor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=350
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("Groq strategy error:", e)
        return _fallback_strategy(question)



def _fallback_strategy(question):
    stocks = [
        "John Keells Holdings (JKH)",
        "Ceylon Tobacco Company (CTC)",
        "Distilleries Company of Sri Lanka (DCSL)",
        "Commercial Bank of Ceylon (COMB)",
        "Sampath Bank (SAMPATH)"
    ]

    allocation = [
        "40% to JKH or CTC for long-term growth",
        "30% to DCSL or COMB for income generation",
        "30% to SAMPATH for a balanced portfolio"
    ]

    stock_list = "\n".join([f"{i+1}. {s}" for i, s in enumerate(stocks)])
    allocation_list = "\n".join([f"* {a}" for a in allocation])

    return f"""
General Investment Guidance:

As a Sri Lankan investment advisor, I recommend considering the following low-risk stocks for a diversified portfolio:

{stock_list}

Suggested Allocation:

{allocation_list}

This is educational guidance only.
"""

