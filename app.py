"""
Lingua Franca — Flask translation web application.

All application code lives in this single file. The codebase will be
split into modules later if the project grows (see project specification
document).

Translation is powered by Google Cloud Translation API. Language detection
runs locally via the langdetect library to avoid network latency during
typing.
"""

import os

from flask import Flask, jsonify, render_template
from dotenv import load_dotenv

# Load environment variables from .env (located at the project root)
load_dotenv()

GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")

app = Flask(__name__)


# -----------------------------------------------------------------------------
# Business logic
# -----------------------------------------------------------------------------

def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    """
    Translate `text` from `source_lang` to `target_lang` via Google Cloud
    Translation API.

    Language codes follow the ISO 639-1 standard (e.g. 'fr', 'en', 'es').

    Args:
        text: the text to translate.
        source_lang: source language code (ISO 639-1).
        target_lang: target language code (ISO 639-1).

    Returns:
        The translated text as a string.

    To be implemented in sprint 1.
    """
    raise NotImplementedError("To be implemented in sprint 1")


def detect_language(text: str) -> str:
    """
    Detect the language of `text` using the local langdetect library.

    Args:
        text: the text to analyze (ideally at least a few words).

    Returns:
        The detected ISO 639-1 language code (e.g. 'fr', 'en').

    To be implemented in sprint 3.
    """
    raise NotImplementedError("To be implemented in sprint 3")


# -----------------------------------------------------------------------------
# Routes
# -----------------------------------------------------------------------------

@app.route("/")
def index():
    """Serve the main translation page."""
    return render_template("index.html")


@app.route("/translate", methods=["POST"])
def translate():
    """
    Translate a text from a source language to a target language.

    Expected JSON body:
        {
            "text": "...",
            "source_lang": "fr",
            "target_lang": "en"
        }
    """
    return jsonify({"error": "Endpoint to be implemented in sprint 1"}), 501


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
