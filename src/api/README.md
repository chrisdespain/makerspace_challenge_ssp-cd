# Chat API Backend

A FastAPI service that proxies chat messages to the OpenAI API. The system prompt configures a deliberately sarcastic "mental coach" persona, consumed by the Emotional Helpdesk frontend.

## Prerequisites

- The [`uv`](https://github.com/astral-sh/uv) package manager (`pip install uv`). `uv` provisions Python 3.12 automatically for this project.
- An OpenAI API key in the `OPENAI_API_KEY` environment variable when running the server.

## Setup

Run all commands from the repository root.

1. Install dependencies into a local `uv`-managed virtual environment:

    ```
    uv sync
    ```

2. (Optional) Activate the virtual environment to run commands manually:

    ```
    source .venv/bin/activate    # Windows: .venv\Scripts\activate
    ```

`uv` creates `.venv/` on first sync and downloads Python 3.12 if it is not already available.

## Running the server

```
uv run uvicorn src.api.index:app --reload
```

The server runs on http://localhost:8000 with auto-reload enabled for development.

**NOTE:** Set `OPENAI_API_KEY` in your shell before launching the server:

```
export OPENAI_API_KEY=sk-your-key-here
```

If you hit an "Address already in use" error, free port 8000:

```
lsof -ti:8000 | xargs kill -9
```

## API endpoints

### Chat

- URL: `/api/chat`
- Method: POST
- Request body:

    ```
    {
        "message": "string"
    }
    ```

- Response:

    ```
    {
        "reply": "string"
    }
    ```

### Root

- URL: `/`
- Method: GET
- Response: `{"status": "ok"}`

## Interactive API documentation

With the server running, FastAPI serves:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## CORS

The API accepts requests from any origin (`*`). Adjust this in `index.py` to restrict access to specific domains.

## Error handling

Errors — a missing API key, OpenAI API errors, and general server errors — return a 500 status code with a message in the `detail` field.

## Testing the endpoint

With the server running:

```
curl -X POST http://127.0.0.1:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

The response is a JSON object with the reply:

```
{
  "reply": "..."
}
```
