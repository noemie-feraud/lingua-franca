# Lingua Franca

> *The past, the present and the future walked into a bar. It was tense.*

Lingua Franca is a web application that lets users translate text between
many languages. Users type text in a left-hand input field, choose source
and target languages from dropdowns, and read the translation in a
right-hand output field. When the source language is unknown, an
auto-detection feature identifies it on the fly.

The project is built as part of an educational assignment at La Plateforme.
It demonstrates how to integrate an external AI service — Google Cloud
Translation — into a custom Flask web application, while exposing its own
REST API for programmatic access.

## Tech stack

- **Backend**: Flask (Python 3.10+)
- **Translation service**: Google Cloud Translation API
- **Language detection**: langdetect (local, no network call)
- **Frontend**: Jinja templates, vanilla CSS and JavaScript

## Getting started

### Prerequisites

- Python 3.10 or higher
- A Google Cloud Platform account with the Cloud Translation API enabled
- A service account JSON key with the `Cloud Translation API User` role

### Installation

Clone the repository and create a virtual environment:

```bash
git clone https://github.com/<your-username>/lingua-franca.git
cd lingua-franca

python -m venv venv
source venv/bin/activate          # macOS / Linux
# venv\Scripts\activate           # Windows

pip install -r requirements.txt
```

Set up credentials. Place your Google Cloud service account JSON file
inside a `credentials/` folder at the project root (this folder is
git-ignored). Then copy the environment template and fill in the values:

```bash
cp .env.example .env
# Edit .env to point to your JSON file and set your project ID
```

### Running the app

```bash
python app.py
```

The application will be available at <http://localhost:5000>.

## Project structure

```
.
├── app.py              Flask application (routes + business logic)
├── templates/
│   └── index.html      Main page
├── credentials/        Google Cloud credentials (git-ignored)
├── requirements.txt    Python dependencies
├── .env.example        Environment variables template
└── .gitignore
```

The project intentionally starts with a flat structure. Modules will be
extracted only when a real need arises.

## REST API

The application exposes its own REST endpoints. They can be consumed
programmatically by any HTTP client (not only the bundled web UI).

| Method | Endpoint     | Description                                |
| ------ | ------------ | ------------------------------------------ |
| GET    | `/`          | Serve the main HTML page                   |
| POST   | `/translate` | Translate text between two languages       |
| POST   | `/detect`    | Detect the language of a given text        |

Detailed request and response formats are documented in `docs/API.md`
(coming soon).

## Project status

- [x] Sprint 0 — Specification and setup
- [ ] Sprint 1 — Core translation function
- [ ] Sprint 2 — Basic web interface
- [ ] Sprint 3 — Dynamic language detection
- [ ] Sprint 4 — Visual identity and styling
- [ ] Sprint 5 — Polish and delivery

## License

Educational project — no public license at this stage.
