FROM python:3.11-slim
WORKDIR /app

# Install uv and project dependencies
RUN python3 -m pip install --upgrade pip
RUN pip install --no-cache-dir uv

COPY pyproject.toml ./
RUN uv pip install --system -r pyproject.toml

COPY .env .
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
