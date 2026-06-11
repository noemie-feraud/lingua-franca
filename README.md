# Traducteur multilingue Flask

Application web de traduction automatique. Front et back en Flask, modèle
NLLB-200 de Meta consommé via l'API Hugging Face, détection de langue
locale via `langdetect`.

## Mise en route

```bash
python -m venv venv
source venv/bin/activate          # sous Windows : venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env              # puis éditer .env pour y mettre la clé HF
python app.py
```

L'application tourne ensuite sur http://localhost:5000.

Pour la clé Hugging Face : créer un compte gratuit sur https://huggingface.co,
puis générer un token avec le rôle `read` dans `Settings > Access Tokens`.

## Structure

```
.
├── app.py              Application Flask (routes + logique métier)
├── templates/
│   └── index.html      Page principale
├── requirements.txt    Dépendances Python
├── .env.example        Template des variables d'environnement
└── .gitignore
```

On démarre volontairement sur une structure minimale. 

## Avancement

- [x] Sprint 0 : cadrage et setup
- [ ] Sprint 1 : fonction `translate_text` opérationnelle
- [ ] Sprint 2 : interface complète (deux zones + sélecteurs)
- [ ] Sprint 3 : détection automatique dynamique
- [ ] Sprint 4 : différenciation (OCR, saisie vocale)
- [ ] Sprint 5 : polissage et livraison
