# Team Story Announcement Board

This project is a simple web app that shows creative stories about your team's AI education projects.

## Features

- `/admin` page lets you enter context items like projects, students, educators, techniques, and results.
- `/board` page displays a story that updates every 5 minutes using OpenAI's `gpt-4.1-nano` model to combine your context items.

## Running

1. Create a virtual environment and install dependencies using [uv](https://github.com/astral-sh/uv):

```bash
uv venv
source .venv/bin/activate # Corrected path for venv activation
uv pip install -r pyproject.toml # Installs dependencies from pyproject.toml
```

2. Set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY='your-openai-api-key'
```

3. Start the server:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

3. Visit `http://localhost:8000/admin` to add context items.
4. Open `http://localhost:8000/board` on the big monitor to display stories.

Set your OpenAI API key in the `OPENAI_API_KEY` environment variable before running the app so announcements can be generated using the API. For local development, you can place this in a `.env` file at the root of the project, and it will be loaded if you haven't removed the `python-dotenv` loading from `main.py`.

Stories are generated on demand, so the board will always show something new when it refreshes.

## Docker

You can run the application in a container. The application inside the Docker container relies _exclusively_ on environment variables for configuration.

1. Build the image (optional, as CI pushes to GHCR):
   ```bash
   docker build -t teamstory .
   ```
2. Run the image, providing your API key:
   ```bash
   docker run -p 8000:8000 -e OPENAI_API_KEY='your-openai-api-key' ghcr.io/${{ github.repository }}:latest
   ```
   Replace `${{ github.repository }}` with your `username/repository_name` if running manually and not in a GitHub Action context (e.g., `leonvanbokhorst/teamstory`).

## Continuous Integration

The CI workflow in `.github/workflows/ci.yml` performs the following:

- Installs dependencies using [uv](https://github.com/astral-sh/uv).
- On pushes to the `main` branch:
  - Builds a multi-platform Docker image (supporting `linux/amd64` and `linux/arm64`).
  - Publishes the Docker image to the GitHub Container Registry (GHCR) at `ghcr.io/your-username/your-repository-name:latest`.

You can pull the latest image directly from GHCR.
