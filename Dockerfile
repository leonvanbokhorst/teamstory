FROM python:3.11-slim
WORKDIR /app

# Install uv and project dependencies
RUN pip install uv

COPY . .
RUN uv pip install --system .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
