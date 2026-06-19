from flask import Flask, request, jsonify, render_template
from gemini_ai import ask_ai
import time

LAST_CALL = 0
COOLDOWN = 12 

def safe_ai_call(prompt):
    global LAST_CALL
    now = time.time()
    if now - LAST_CALL < COOLDOWN:
        return "Please wait a few seconds before asking again."
    LAST_CALL = now
    return ask_ai(prompt)


import os

base_dir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(base_dir, 'templates')

app = Flask(__name__, template_folder=template_dir)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/command", methods=["POST"])
def command():
    data = request.get_json(force=True)
    cmd = data.get("command", "").strip().lower()

    print("Received:", cmd)

    if not cmd:
        return jsonify({
            "response": "I didn't catch that. Please say the command again.",
            "understood": False
        })

    ai_response = ask_ai(cmd)
    return jsonify({
        "response": ai_response,
        "understood": True,
        "source": "gemini"
    })



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
