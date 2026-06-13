import os

from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv

# Load environment variables from .env (located at the project root)
load_dotenv()

GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")

app = Flask(__name__)


# Business logic

def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    """
    Translate `text` from `source_lang` to `target_lang` via Google Cloud
    Translation API.

    TODO sprint 1: replace this mock with a real Google Cloud Translation call.
    """
    # Temporary mock implementation — lets the UI work end-to-end before
    # the Google API key is available.
    return f"[MOCK {source_lang} -> {target_lang}] {text}"


def detect_language(text: str) -> str:
    """
    Detect the language of `text` using the local langdetect library.
    """
    raise NotImplementedError("To be implemented in sprint 3")


# Routes

@app.route("/")
def index():
    """Serve the main translation page."""
    return render_template("index.html")


@app.route("/translate", methods=["POST"])
def translate():
    """
    Translate a text from a source language to a target language.
    """
    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    text = payload.get("text")
    source_lang = payload.get("source_lang")
    target_lang = payload.get("target_lang")

    if not text or not isinstance(text, str):
        return jsonify({"error": "Field 'text' is required and must be a string"}), 400
    if not source_lang:
        return jsonify({"error": "Field 'source_lang' is required"}), 400
    if not target_lang:
        return jsonify({"error": "Field 'target_lang' is required"}), 400

    try:
        translation = translate_text(text, source_lang, target_lang)
    except Exception as exc:
        # Catch-all to avoid leaking stack traces to the client.
        # Will be refined in sprint 5 (error handling).
        return jsonify({"error": f"Translation failed: {exc}"}), 500

    return jsonify({"translation": translation}), 200


@app.route("/detect", methods=["POST"])
def detect():
    """
    Detect the language of a given text.

    Expected JSON body:
        { "text": "..." }
    """
    return jsonify({"error": "Endpoint to be implemented in sprint 3"}), 501


if __name__ == "__main__":
    app.run(debug=True)
