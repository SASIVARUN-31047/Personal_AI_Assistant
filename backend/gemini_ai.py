import os
from google import genai
MODEL_CHAIN = [
    "models/gemini-3.1-flash-lite", 
    "models/gemini-2.5-flash-lite", 
]

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

    last_error = None

    for model_name in MODEL_CHAIN:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=[SYSTEM_PROMPT, prompt]
            )
            print("OK via:", model_name)
            return response.text.strip()

        except Exception as e:
            last_error = e
            err = str(e).lower()
            print(f"GEMINI ERROR ({model_name}):", repr(e))
            continue

    # All models failed — return a clear message based on the last error.
    err = str(last_error).lower() if last_error else ""
    if "429" in err or "quota" in err or "rate" in err:
        return "I'm getting too many requests right now. Wait a few seconds and try again."
    if "timeout" in err or "deadline" in err:
        return "That took too long to process. Please try again."
    if "api key" in err or "permission" in err or "401" in err or "403" in err:
        return "There's a problem with my API key. Check the Gemini key on Vercel."
    if "not found" in err or "404" in err or "not supported" in err:
        return "The AI model name seems invalid. Check the model names in the code."
    return f"Error: {type(last_error).__name__}"
