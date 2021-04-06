# FinMindBook 5.5.4

### run rabbitmq
    docker-compose -f rabbitmq.yml up -d

### install package
    pipenv sync

### run worker
    pipenv run celery -A worker worker --loglevel=info

### sent task
    pipenv run python producer.py