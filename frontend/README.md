# Emotional Helpdesk — Frontend

> File your feelings. We'll get back to you.

A Next.js chat interface styled as a corporate IT support ticket system. You file emotional support tickets (`EMO-XXXX`), set priority levels, and get responses from `[HELPDESK BOT] (Level 1 Support)`.

## Local Development

### 1. Backend (port 8000)

From the project root:

```bash
uv run uvicorn api.index:app --reload
```

### 2. Frontend (port 3000)

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Environment Variables

Create `frontend/.env.local`:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Root `.env` (for backend):

```
OPENAI_API_KEY=sk-...
```

## Features

- File emotional support tickets with auto-generated `EMO-XXXX` IDs
- Priority levels: LOW / MEDIUM / HIGH / CRITICAL (with absurd labels)
- Ticket status: OPEN → IN PROGRESS → RESOLVED (click badge to cycle)
- Sidebar with full ticket history, persisted in localStorage
- Star/favorite agent responses
- Export any ticket as a Markdown file
- Copy responses to clipboard
- Dark / light mode (persisted)
- Suggested "common issues" prompts on new tickets
- Mobile responsive with collapsible sidebar
