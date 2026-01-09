import os
from dotenv import load_dotenv
from google import genai
from pathlib import Path
import json
import re

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY)


def generate_quiz(text: str):
    prompt = f"""
You are an educational quiz generator.

From the Wikipedia article below, generate 5 quiz questions.

Each question must include:
- question
- 4 options
- correct_answer
- difficulty (easy/medium/hard)
- explanation

Also suggest 4 related Wikipedia topics.

Return ONLY valid JSON in this format:
{{
 "quiz": [...],
 "related_topics": [...]
}}

Article:
{text[:6000]}
"""

    response = client.models.generate_content(
        model="models/gemini-flash-latest",
        contents=prompt
    )

    raw = response.text.strip()
    clean = re.sub(r"```json|```", "", raw)

    try:
        return json.loads(clean)
    except Exception as e:
        print("LLM JSON ERROR")
        print(raw)

        return {
            "quiz": [],
            "related_topics": [],
            "error": "LLM did not return valid JSON"
        }
