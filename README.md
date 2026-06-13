# Lingua Franca

> *The past, the present and the future walked into a bar. It was tense.*

Lingua Franca is a web application that lets users translate text between
many languages. Users type text in a left-hand input field, choose source
and target languages from dropdowns, and read the translation in a
right-hand output field. When the source language is unknown, an
auto-detection feature identifies it on the fly as the user types.

The project is built as part of an educational assignment at La Plateforme.
It demonstrates how to integrate an external AI service — the MyMemory
Translation API — into a custom Flask web application, while exposing its
own REST API for programmatic access.

## Features

- Translate text between 12 languages: French, English, Spanish, German,
  Italian, Portuguese, Dutch, Polish, Russian, Japanese, Chinese, Arabic
- Auto-detect the source language while the user types (with a 500 ms
  debounce to avoid hammering the server)
- Display the detected language in real time
- Expose all translation features as a REST API consumable by any HTTP client

## Tech stack

- **Backend**: Flask (Python 3.10+)
- **Translation service**: MyMemory Translation API (free tier, no signup)
- **Language detection**: langdetect (local, no network call)
- **Frontend**: Jinja templates, vanilla CSS and JavaScript

## Getting started

### Prerequisites

- Python 3.10 or higher
- Optionally, a valid email address to lift the MyMemory daily quota
  from 5,000 characters to ~50,000 words

### Installation

Clone the repository and create a virtual environment:

```bash
git clone https://github.com/noemie-feraud/lingua-franca.git
cd lingua-franca

python -m venv venv
source venv/bin/activate          # macOS / Linux
# venv\Scripts\activate           # Windows

pip install -r requirements.txt
```

Configure environment variables (optional). The application works out of
the box in anonymous mode. To raise the daily quota, copy the template
and provide an email:

```bash
cp .env.example .env
# Edit .env and set MYMEMORY_EMAIL to your email address
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
├── static/
│   ├── css/
│   │   └── style.css   Stylesheet (Nunito, golden-ratio scale)
│   └── js/
│       └── main.js     Frontend logic (translate, detect, debounce)
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

### POST /translate

Request body:

```json
{
  "text": "Bonjour le monde",
  "source_lang": "fr",
  "target_lang": "en"
}
```

The `source_lang` and `target_lang` fields accept ISO 639-1 codes. Auto
detection must be performed via `/detect` before calling `/translate`.

Success response (200):

```json
{ "translation": "Hello world" }
```

Error responses: `400` for malformed input, `502` for upstream API
failure, `500` for unexpected server errors.

### POST /detect

Request body:

```json
{ "text": "Bonjour le monde" }
```

Success response (200):

```json
{ "language": "fr" }
```

When detection is uncertain (text too short or language outside the
supported set), the API returns `200` with `{ "language": null }`
rather than an error.

For the full API reference including all error cases, response formats,
and example curl commands, see [docs/API.md](docs/API.md).

## Project status

- [x] Sprint 0 — Specification and setup
- [x] Sprint 1 — Core translation function
- [x] Sprint 2 — Basic web interface
- [x] Sprint 3 — Dynamic language detection
- [x] Sprint 4 — Visual identity and styling
- [ ] Sprint 5 — Polish and delivery

## Authors

This project was made by:

- Assmine AHAMADA
- Antuat ABDALLAH
- Noémie FERAUD

## License

Educational project — no public license at this stage.
