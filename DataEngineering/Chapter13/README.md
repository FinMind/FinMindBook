# FinMindBook 13

### run redis
    docker-compose -f redis.yml up -d

### install package
    pipenv sync

### run worker
    pipenv run celery -A worker worker --loglevel=info

### sent task
    pipenv run python producer.py