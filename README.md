# Weather API

# To Run project locally

## Export environment variables

```bash
export $(cat .env | xargs)
```

## Run with poetry locally

```bash
poetry run uvicorn weather_api.main:app --reload
```

## Build docker compose

```bash
sudo docker compose build --no-cache
```

## Run All Services

```bash
sudo docker compose up api redis minio
```

## Add minio bucket

### login with

- username: minioadmin
- password: minioadmin

### add bucket weather-data

## Run test service for system tests

```bash
sudo docker compose run test
```

## API Documentation Endpoint

http://127.0.0.1:8000/docs
