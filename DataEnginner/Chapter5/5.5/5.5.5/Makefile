
create-mysql:
	docker-compose -f mysql.yml up -d

create-rabbitmq:
	docker-compose -f rabbitmq.yml up -d

install-python-env:
	pipenv sync

run-celery:
	pipenv run celery -A financialdata.tasks.worker worker --loglevel=info

