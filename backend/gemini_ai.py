import os
from google import genai
from google.genai import types

# Tries the first model; if it fails, falls back to the next one.
MODEL_CHAIN = [
    "models/gemini-3.1-flash-lite",   # newer, try first
    "models/gemini-2.5-flash-lite",   # confirmed 1,000/day fallback
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
- In a chat, remember what we discussed earlier and answer follow-ups in context.
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


def _error_message(last_error):
    """Turn an exception into a clear, user-facing message."""
    err = str(last_error).lower() if last_error else ""
    if "429" in err or "quota" in err or "rate" in err:
        return "I'm getting too many requests right now. Wait a few seconds and try again."
    if "timeout" in err or "deadline" in err:
        return "That took too long to process. Please try again."
    if "api key" in err or "permission" in err or "401" in err or "403" in err:
        return "There's a problem with my API key. Check the Gemini key on Vercel."
    if "not found" in err or "404" in err or "not supported" in err:
        return "The AI model name seems invalid. Check the model names in the code."
    return f"Error: {type(last_error).__name__}" if last_error else "Something went wrong."


# ---------- VOICE: single standalone command (no memory) ----------
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
            print(f"GEMINI ERROR ({model_name}):", repr(e))
            continue

    return _error_message(last_error)


# ---------- TEXT CHAT: full conversation with memory ----------
def ask_ai_chat(messages) -> str:
    """
    messages: a list like
      [{"role": "user", "text": "..."}, {"role": "model", "text": "..."}, ...]
    The whole history is sent each time so Gemini remembers the conversation.
    """
    client = get_client()
    if not client:
        return "SERVER ERROR: The Gemini API Key is missing on Vercel. Please add it to Environment Variables and Redeploy!"

    # Build conversation contents with proper roles
    contents = []
    for m in messages:
        role = "user" if m.get("role") == "user" else "model"
        text = (m.get("text") or "").strip()
        if not text:
            continue
        contents.append(types.Content(role=role, parts=[types.Part(text=text)]))

    if not contents:
        return "Please type a message."

    last_error = None
    for model_name in MODEL_CHAIN:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=contents,
                config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT)
            )
            print("CHAT OK via:", model_name)
            return response.text.strip()
        except Exception as e:
            last_error = e
            print(f"GEMINI CHAT ERROR ({model_name}):", repr(e))
            continue

    return _error_message(last_error)
