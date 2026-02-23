FROM python:3.12-slim

WORKDIR /app
ENV PYTHONPATH=/app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=2.0.1
ENV PYTEST_VERSION=9.0.2
ENV PYTEST_VERSION_ASYNCIO==1.3.0
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"
RUN pip install pytest --no-cache-dir "pytest==$PYTEST_VERSION"
RUN pip install pytest-asyncio --no-cache-dir "pytest-asyncio==$PYTEST_VERSION_ASYNCIO"
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock README.md ./

RUN poetry install --no-interaction --no-ansi --all-groups --no-root

COPY weather_api/ ./weather_api/
COPY tests/ ./tests/

EXPOSE 8000
CMD ["uvicorn", "weather_api.main:app", "--host", "0.0.0.0", "--port", "8000"]