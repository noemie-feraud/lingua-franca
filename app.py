import os

import requests
from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
from langdetect import detect, DetectorFactory, LangDetectException

# Make langdetect deterministic so the same input always gives the same
# output. Without this, results may vary slightly between calls.
DetectorFactory.seed = 0

# Load environment variables from .env (located at the project root)
load_dotenv()

MYMEMORY_API_URL = "https://api.mymemory.translated.net/get"
MYMEMORY_EMAIL = os.getenv("MYMEMORY_EMAIL", "")

app = Flask(__name__)


# Business logic

def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    """
    Translate `text` from `source_lang` to `target_lang` via the MyMemory
    Translation API.
    """
    if source_lang == "auto":
        raise ValueError(
            "MyMemory requires an explicit source language. "
            "Detect it client-side first, then call this function."
        )

    params = {
        "q": text,
        "langpair": f"{source_lang}|{target_lang}",
    }
    if MYMEMORY_EMAIL:
        params["de"] = MYMEMORY_EMAIL

    response = requests.get(MYMEMORY_API_URL, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()

    # MyMemory may return HTTP 200 with a logical error in the payload.
    # The status field is sometimes returned as int, sometimes as string.
    status = int(data.get("responseStatus", 0))
    if status != 200:
        details = data.get("responseDetails", "unknown error")
        raise RuntimeError(f"MyMemory rejected the request: {details}")

    return data["responseData"]["translatedText"]


def detect_language(text: str) -> str:
    """
    Detect the language of `text` using the local langdetect library.
    """
    return detect(text)


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
    if source_lang == "auto":
        return jsonify({"error": "Source language must be detected before translating"}), 400

    try:
        translation = translate_text(text, source_lang, target_lang)
    except requests.RequestException as exc:
        return jsonify({"error": f"Translation service unavailable: {exc}"}), 502
    except RuntimeError as exc:
        return jsonify({"error": str(exc)}), 502
    except Exception as exc:
        # Catch-all to avoid leaking stack traces to the client.
        return jsonify({"error": f"Unexpected error: {exc}"}), 500

    return jsonify({"translation": translation}), 200


@app.route("/detect", methods=["POST"])
def detect_route():
    """
    Detect the language of a given text.
    """
    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    text = payload.get("text")
    if not text or not isinstance(text, str):
        return jsonify({"error": "Field 'text' is required and must be a string"}), 400

    try:
        language = detect_language(text)
    except LangDetectException:
        return jsonify({"error": "Could not detect language (text too short or ambiguous)"}), 400

    return jsonify({"language": language}), 200


if __name__ == "__main__":
    app.run(debug=True)
