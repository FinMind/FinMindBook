# FinMindBook 13

### run redis
    docker compose -f redis.yml up -d

### install package
    uv sync

### run worker
    uv run --env-file=.env celery -A worker worker --loglevel=info

### sent task
    uv run --env-file=.env python producer.py