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

**NOTE:** `APP_ACCESS_CODE` is optional locally. Leave it unset for normal local dev (the access gate stays off); set it only to test the gate locally.

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

## Deployment (Vercel)

The repo deploys as-is — no restructuring needed:

- `api/index.py` is auto-detected as a Python serverless function at the repo root.
- The frontend builds via `vercel.json` (`framework: nextjs`, `cd frontend && npm run build`, output `frontend/.next`).
- `/api/*` is routed to the Python function via the `rewrites` in `vercel.json`.

### One-time setup (Vercel CLI)

```
npm i -g vercel
vercel login
vercel link        # link this folder to a Vercel project; creates .vercel/
```

**NOTE:** `vercel link` writes a local `.vercel/` directory holding the project link. It's already in `.gitignore` — keep it untracked (do not commit it).

### GitHub linkage (auto-deploy on push)

Connect the Vercel project to the GitHub repo so deployments happen on push — no manual step needed afterward:

- Pushing a branch creates a **Preview** deployment; pushing/merging to the production branch deploys to **Production**.
- Connect once, either way:
  - Dashboard: Vercel → Add New → Project → import the GitHub repo.
  - CLI (from the linked repo): `vercel git connect`.

After linkage, the normal flow is just `git push`.

### Manual deploy (Vercel CLI)

```
vercel            # build and deploy a Preview; prints a preview URL
vercel --prod     # deploy to Production
```

### Environment variables

Required in Production. Set via the dashboard (Settings → Environment Variables) or the CLI:

```
vercel env add OPENAI_API_KEY production
vercel env add APP_ACCESS_CODE production
vercel env pull            # optional: pull Production vars into a local env file
```

```
OPENAI_API_KEY     the OpenAI key the backend calls with
APP_ACCESS_CODE    the shared code that gates access to the app
```

**NOTE:** Environment-variable changes only take effect on a new deployment — after adding or changing them, redeploy with `vercel --prod` (or push, if GitHub-linked).

## Auth & key maintenance

### OpenAI key (`OPENAI_API_KEY`)

The key is stored only in Vercel environment variables — never committed to the repo. If the key is short-lived, the app starts returning 500s once it expires; rotate it and redeploy:

- Dashboard: Settings → Environment Variables → edit `OPENAI_API_KEY`, then redeploy.
- CLI: `vercel env rm OPENAI_API_KEY production` then `vercel env add OPENAI_API_KEY production`, then `vercel --prod`.

**NOTE:** Do not hard-code the key in source — it would persist in git history even if later removed.

### Access gate (`APP_ACCESS_CODE`)

When `APP_ACCESS_CODE` is set, the app shows a code screen before it can be used. Share the code to grant access; change it (and redeploy) to revoke everyone. The code is entered once per browser and stored locally.

- This is an **app-level** gate (a plain env var checked in `api/index.py`), not Vercel Deployment Protection — so it works on any plan, including Hobby, and grants access by shared code rather than per-account invites.
- It is inactive locally: with `APP_ACCESS_CODE` unset, the gate is open and the backend uses your OS `OPENAI_API_KEY` — local dev needs neither.

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
