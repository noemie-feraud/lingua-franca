# Lingua Franca REST API

This document describes the HTTP API exposed by the Lingua Franca
application. Any HTTP client (browser, curl, Postman, another program)
can consume these endpoints. The bundled web interface is one such
client among others.

## General information

**Base URL**: `http://localhost:5000` (development) — adjust to your
deployment URL in production.

**Exchange format**: JSON for both requests and responses. All POST
endpoints expect a request body with `Content-Type: application/json`.

**Authentication**: none. The API is open and stateless.

**Character encoding**: UTF-8.

## Endpoints overview

| Method | Path         | Purpose                                  |
| ------ | ------------ | ---------------------------------------- |
| GET    | `/`          | Serve the web interface (HTML)           |
| POST   | `/translate` | Translate text between two languages     |
| POST   | `/detect`    | Detect the language of a text            |

The next sections describe each endpoint in detail.

## GET /

Returns the main web page as `text/html`. This endpoint is intended for
human users opening the application in a browser; programmatic clients
should use `/translate` and `/detect` directly.

**Request**: no parameters.

**Response (200)**: HTML page.

## POST /translate

Translates a text from a source language to a target language using the
MyMemory Translation API.

**Request body**:

```json
{
  "text": "Bonjour le monde",
  "source_lang": "fr",
  "target_lang": "en"
}
```

Field reference:

| Field         | Type   | Required | Description                                |
| ------------- | ------ | -------- | ------------------------------------------ |
| `text`        | string | yes      | The text to translate. Must be non-empty.  |
| `source_lang` | string | yes      | ISO 639-1 code of the source language.     |
| `target_lang` | string | yes      | ISO 639-1 code of the target language.     |

The special value `"auto"` is **not** accepted for `source_lang`.
Callers must detect the source language first via `/detect`.

**Supported language codes**: `fr`, `en`, `es`, `de`, `it`, `pt`, `nl`,
`pl`, `ru`, `ja`, `zh`, `ar`. Other codes may work if MyMemory supports
them, but our application UI only exposes these twelve.

**Success response (200)**:

```json
{
  "translation": "Hello world"
}
```

**Example request**:

```bash
curl -X POST http://localhost:5000/translate \
  -H "Content-Type: application/json" \
  -d '{"text":"Bonjour le monde","source_lang":"fr","target_lang":"en"}'
```

**Error responses**: see the [Error handling](#error-handling) section
below.

## POST /detect

Detects the language of a given text using a two-stage cascade:

1. Local detection with the `langdetect` Python library (fast, no
   network call) — used when the text is at least 20 characters long
   and the detected language belongs to our supported set.
2. Fallback to MyMemory's `autodetect` feature when local detection is
   unreliable or returns a language outside the supported set.
3. When both stages fail, the API returns a `null` language rather than
   an error: detection uncertainty is a legitimate outcome, not a
   client mistake.

**Request body**:

```json
{
  "text": "Bonjour le monde"
}
```

Field reference:

| Field  | Type   | Required | Description                          |
| ------ | ------ | -------- | ------------------------------------ |
| `text` | string | yes      | The text to analyze. Must be non-empty. |

**Success response (200) — detection succeeded**:

```json
{
  "language": "fr"
}
```

**Success response (200) — detection uncertain**:

```json
{
  "language": null
}
```

A `null` value means we could not confidently identify a supported
language for the given text. Clients should treat this as "unknown"
and not display a misleading detection result.

**Example request**:

```bash
curl -X POST http://localhost:5000/detect \
  -H "Content-Type: application/json" \
  -d '{"text":"Bonjour le monde"}'
```

## Error handling

Error responses share a common JSON structure:

```json
{
  "error": "Human-readable description of what went wrong"
}
```

HTTP status codes follow REST conventions:

| Status | Meaning                                                       |
| ------ | ------------------------------------------------------------- |
| 400    | Malformed request: missing body, missing field, wrong type    |
| 500    | Unexpected server error                                       |
| 502    | The upstream translation service (MyMemory) is unavailable or returned a logical error |

**Why 502 and not 500 on upstream failures**: by convention, `502 Bad
Gateway` indicates that a server acting as a proxy received an invalid
response from the upstream server. Since our `/translate` endpoint is
essentially a wrapper around MyMemory, returning 502 when MyMemory
fails accurately conveys where the problem originates. This lets
clients distinguish "your request was bad" (400), "our code crashed"
(500), and "the service we depend on is down" (502).

**Example error response (missing text field)**:

```json
{
  "error": "Field 'text' is required and must be a string"
}
```

**Example error response (MyMemory unavailable)**:

```json
{
  "error": "Translation service unavailable: HTTPSConnectionPool..."
}
```

## Implementation notes

The API is implemented in `app.py` using Flask. Translation is delegated
to the MyMemory Translation API
([documentation](https://mymemory.translated.net/doc/spec.php)).
Language detection combines the `langdetect` Python library with the
MyMemory autodetect feature, as described in the `/detect` section.

For development setup, environment configuration, and running the
application locally, see the main `README.md` file at the project root.
