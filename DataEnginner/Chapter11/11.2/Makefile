

create-postgres-volume:
	docker volume create --name=postgres

create-redis-redash-volume:
	docker volume create --name=redis_redash

create-db:
	docker-compose run --rm server create_db

create-db-by-python:
	# docker exec -it redash_server_1 bash
	python /app/manage.py database create_tables

up:
	docker-compose -f docker-compose.yml up

up-d:
	docker-compose -f docker-compose.yml up -d

down:
	docker-compose -f docker-compose.yml down

# test
test-cov:
	pipenv run pytest --cov-report term-missing --cov-config=.coveragerc --cov=./${PROJECT_NAME}/ tests/

test:
	pipenv run pytest

# other
format:
	black -l 80 redash/* tests/* example/*
