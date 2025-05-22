# Team Story Announcement Board

This project is a simple web app that shows creative stories about your team's AI education projects.

## Features
- `/admin` page lets you enter context items like projects, students, educators, techniques, and results.
- `/board` page displays a story that updates every 5 minutes using OpenAI's `gpt-4.1-nano` model to combine your context items.

## Running

1. Create a virtual environment and install dependencies using [uv](https://github.com/astral-sh/uv):

```bash
uv venv
source venv/bin/activate
uv pip install -r pyproject.toml
```

2. Start the server:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

3. Visit `http://localhost:8000/admin` to add context items.
4. Open `http://localhost:8000/board` on the big monitor to display stories.

Set your OpenAI API key in the `OPENAI_API_KEY` environment variable before running the app so announcements can be generated using the API.

Stories are generated on demand, so the board will always show something new when it refreshes.

## Docker

You can run the application in a container (the Docker image uses `uv` to install dependencies):


```bash
docker build -t teamstory .
docker run -p 8000:8000 -e OPENAI_API_KEY=your-key teamstory
```

## Continuous Integration

The CI workflow installs dependencies with [uv](https://github.com/astral-sh/uv),
runs the unit tests and, when changes are pushed to `main`, builds and
publishes a Docker image to the GitHub Container Registry.

