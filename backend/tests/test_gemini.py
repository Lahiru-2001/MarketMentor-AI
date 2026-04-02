from dotenv import load_dotenv
from pathlib import Path
import os
from google import genai

load_dotenv(Path(__file__).parent / "key.env")

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

response = client.models.generate_content(
    model="gemini-1.5-flash",
    contents="Say hello in one sentence"
)

print(response.text)
