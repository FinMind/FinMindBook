# FinMindBook 4.4.3

### run rabbitmq
    docker-compose -f rabbitmq.yml up -d

### install package
    pipenv sync

### run worker
    pipenv run celery -A Worker worker --loglevel=info

### sent task
    pipenv run python Producer.py