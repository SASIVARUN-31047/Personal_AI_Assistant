import os
from google import genai

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

def get_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None
    try:
        return genai.Client(api_key=api_key)
    except Exception as e:
        print("Error initializing client:", e)
        return None

def ask_ai(prompt: str) -> str:
    if not prompt.strip():
        return "Please repeat the command."
        
    client = get_client()
    if not client:
        return "SERVER ERROR: The Gemini API Key is missing on Vercel. Please add it to Environment Variables and Redeploy!"

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
