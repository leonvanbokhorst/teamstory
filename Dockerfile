FROM python:3.11-slim
WORKDIR /app

# Install runtime dependencies using uv
COPY pyproject.toml ./
RUN pip install --no-cache-dir uv \
    && uv pip install -r pyproject.toml

# Copy source
COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
