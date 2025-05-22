# Team Story Announcement Board

This project is a simple web app that shows creative stories about your team's AI education projects.

## Features
- `/admin` page lets you enter context items like projects, students, educators, techniques, and results.
- `/board` page displays a story that updates every 5 minutes using random combinations of your context items.

## Running

1. Install dependencies (FastAPI and Uvicorn are already included in this environment):

```bash
pip install fastapi uvicorn
```

2. Start the server:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

3. Visit `http://localhost:8000/admin` to add context items.
4. Open `http://localhost:8000/board` on the big monitor to display stories.

Stories are generated on demand, so the board will always show something new when it refreshes.
