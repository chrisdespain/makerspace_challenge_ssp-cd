# Emotional Helpdesk — Frontend

A Next.js chat interface styled as a corporate IT support ticket system. Users file emotional support tickets (`EMO-XXXX`), set priority levels, and receive responses from a "Level 1 Support" agent backed by the FastAPI service in `/api`.

## Local development

### Backend (port 8000)

From the project root:

```
uv run uvicorn api.index:app --reload
```

### Frontend (port 3000)

```
cd frontend
npm install
npm run dev
```

Open http://localhost:3000.

## Environment variables

Create `frontend/.env.local`:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Create `.env` in the project root (used by the backend):

```
OPENAI_API_KEY=sk-...
```

## Testing

The suite in `/tests` uses Playwright via the `pytest-playwright` plugin. Each test launches Chromium and drives the running app at http://localhost:3000.

**NOTE:** The backend is not required to run the tests. `tests/conftest.py` mocks `POST /api/chat`, so `uvicorn` and an `OPENAI_API_KEY` are not needed — only the frontend dev server.

One-time setup to install the Chromium browser:

```
playwright install chromium
```

1. Start the frontend dev server (port 3000):

    ```
    cd frontend
    npm run dev
    ```

2. In a second terminal, from the project root, activate the virtual environment and run the tests:

    ```
    source .venv/bin/activate
    pytest tests/ -v
    ```

**NOTE:** Run `pytest` from the project root, not from `frontend/`. The pytest configuration and the `tests/` package resolve relative to the root, and the virtual environment must be active so `pytest`, `playwright`, and the browser are on the path.

Useful variations:

```
pytest tests/test_tickets.py -v    # a single file
pytest tests/ -k sidebar           # tests matching a keyword
pytest tests/ --lf                 # re-run only the last failures
pytest tests/ --headed             # run with a visible browser window
```

## Features

- File emotional support tickets with auto-generated `EMO-XXXX` IDs
- Priority levels: LOW / MEDIUM / HIGH / CRITICAL
- Ticket status: OPEN, IN PROGRESS, RESOLVED (click the badge to cycle)
- Sidebar with full ticket history, persisted in the browser via `localStorage`
- Star agent responses
- Export a ticket as Markdown
- Copy responses to the clipboard
- Dark and light mode (persisted)
- Suggested "common issues" prompts on a new ticket
- Responsive layout with a collapsible sidebar on mobile
