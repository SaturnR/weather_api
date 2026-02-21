# Weather API

# To Run project locally

## Export environment variables

```bash
export $(cat .env | xargs)
```

## Run with poetry

```bash
poetry run uvicorn weather_api.main:app --reload
```
