# -------- Base Image --------
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# -------- System Dependencies --------
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
    && rm -rf /var/lib/apt/lists/*

# -------- Install Poetry --------
ENV POETRY_VERSION=1.8.3

RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

# Disable virtualenv creation (important inside Docker)
RUN poetry config virtualenvs.create false

# -------- Copy Dependency Files First (Layer Caching) --------
COPY pyproject.toml poetry.lock* ./

# Install only main dependencies (no dev)
RUN poetry install --no-interaction --no-ansi --only main

# -------- Copy Application Code --------
COPY app/ ./app/

# -------- Create Non-Root User --------
RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser /app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
