import os
from google import genai

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

MODEL_NAME = "models/gemini-flash-latest"

# 🔒 YOUR CONTROL PROMPT (THIS IS THE BRAIN)
SYSTEM_PROMPT = """
You are Jarvis, my personal AI assistant.

Rules you MUST follow:
- Give short and clear answers by default (3–5 lines).
- Do NOT over-explain unless I say "explain in detail".
- Speak like a calm, professional assistant.
- If the question is technical, explain simply first.
- If I say "stop", immediately stop responding.
- Never say unnecessary greetings.
"""

def ask_ai(prompt: str) -> str:
    if not prompt.strip():
        return "Please repeat the command."

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[
                SYSTEM_PROMPT,
                prompt
            ]
        )
        return response.text.strip()

    except Exception as e:
        print("GEMINI ERROR:", e)
        return "I am unable to respond right now."
