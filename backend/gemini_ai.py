import os
from google import genai

MODEL_NAME = "models/gemini-2.5-flash-lite"

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
            contents=[SYSTEM_PROMPT, prompt]
        )
        return response.text.strip()

    except Exception as e:
        err = str(e).lower()
        print("GEMINI ERROR:", repr(e))
        if "429" in err or "quota" in err or "rate" in err:
            return "I'm getting too many requests right now. Wait a few seconds and try again."
        if "timeout" in err or "deadline" in err:
            return "That took too long to process. Please try again."
        if "api key" in err or "permission" in err or "401" in err or "403" in err:
            return "There's a problem with my API key. Check the Gemini key on Vercel."
        return f"Error: {type(e).__name__}"
