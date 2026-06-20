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
        print("GEMINI ERROR:", repr(e))   # shows the real reason in Vercel logs

        if "429" in err or "quota" in err or "rate" in err:
            return "I'm getting too many requests right now. Wait a few seconds and try again."
        if "timeout" in err or "deadline" in err:
            return "That took too long to process. Please try again."
        if "api key" in err or "permission" in err or "401" in err or "403" in err:
            return "There's a problem with my API key. Check the Gemini key on Vercel."

        return f"Error: {type(e).__name__}"
