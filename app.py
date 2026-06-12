import os

from flask import Flask, jsonify, render_template
from dotenv import load_dotenv

# Load environment variables from .env (located at the project root)
load_dotenv()

GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")

app = Flask(__name__)


# Business logic

def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    raise NotImplementedError("To be implemented in sprint 1")


def detect_language(text: str) -> str:
    raise NotImplementedError("To be implemented in sprint 3")


# Routes

@app.route("/")
def index():
    """Serve the main translation page."""
    return render_template("index.html")


@app.route("/translate", methods=["POST"])
def translate():
    return jsonify({"error": "Endpoint to be implemented in sprint 1"}), 501


@app.route("/detect", methods=["POST"])
def detect():
    """Translate a text from a source language to a target language"""
    return jsonify({"error": "Endpoint to be implemented in sprint 3"}), 501


if __name__ == "__main__":
    app.run(debug=True)
