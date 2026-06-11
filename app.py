"""
Application Flask de traduction multilingue.

Tout le code tient dans ce fichier. Si à l'avenir le projet grossit
(ajout de l'OCR, de la saisie vocale, de la comparaison multi-modèles),
on découpera à ce moment-là — pas avant. Voir notre doc de cadrage.
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


# -----------------------------------------------------------------------------
# Logique métier
# -----------------------------------------------------------------------------

def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    """
    Traduit `text` de `source_lang` vers `target_lang` via l'API Hugging Face.

    NLLB-200 utilise des codes BCP-47 avec script (ex: 'fra_Latn', 'eng_Latn'),
    pas les codes ISO 639-1 classiques. À garder en tête.

    À implémenter au sprint 1.
    """
    raise NotImplementedError("À implémenter au sprint 1")


def detect_language(text: str) -> str:
    """
    Renvoie le code ISO 639-1 de la langue détectée (ex: 'fr', 'en').
    Utilise la lib langdetect en local pour éviter la latence d'un appel API.

    À implémenter au sprint 3.
    """
    raise NotImplementedError("À implémenter au sprint 3")


# -----------------------------------------------------------------------------
# Routes
# -----------------------------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/translate", methods=["POST"])
def translate():
    return jsonify({"error": "Route à implémenter au sprint 1"}), 501


@app.route("/detect", methods=["POST"])
def detect():
    return jsonify({"error": "Route à implémenter au sprint 3"}), 501


if __name__ == "__main__":
    app.run(debug=True)
