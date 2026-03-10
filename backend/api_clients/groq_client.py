import os
from pathlib import Path
from dotenv import load_dotenv

# Load key.env
BASE_DIR = Path(__file__).resolve().parents[1]
ENV_PATH = BASE_DIR / "key.env"
load_dotenv(dotenv_path=ENV_PATH)

try:
    from groq import Groq

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY not found in key.env")

    client = Groq(api_key=api_key)
    GROQ_AVAILABLE = True

except Exception as e:
    client = None
    GROQ_AVAILABLE = False
    print("Groq initialization failed:", str(e))
