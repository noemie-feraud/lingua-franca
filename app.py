"""
Application Flask de traduction multilingue.
"""

import os

from flask import Flask, jsonify, render_template
from dotenv import load_dotenv

# Chargement des variables d'environnement (.env à la racine du projet)
load_dotenv()

HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
HF_MODEL = os.getenv("HUGGINGFACE_MODEL", "facebook/nllb-200-distilled-600M")
HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"

app = Flask(__name__)


# Logique métier

def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    raise NotImplementedError("À implémenter")


def detect_language(text: str) -> str:
    raise NotImplementedError("À implémenter")


# Routes

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/translate", methods=["POST"])
def translate():
    return jsonify({"error": "Route à implémenter"}), 501


@app.route("/detect", methods=["POST"])
def detect():
    return jsonify({"error": "Route à implémenter"}), 501


if __name__ == "__main__":
    app.run(debug=True)
