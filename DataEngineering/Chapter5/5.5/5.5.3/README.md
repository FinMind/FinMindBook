# FinMindBook 5.5.3

### run rabbitmq
    docker-compose -f rabbitmq.yml up -d

### install package
    pipenv sync

### run worker
    pipenv run celery -A worker worker --concurrency=10 --loglevel=info

### sent task
    pipenv run python producer.py