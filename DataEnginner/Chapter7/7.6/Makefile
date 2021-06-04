
create-mysql-volume:
	docker volume create mysql

create-network:
	docker network create --scope=swarm --driver=overlay my_network

deploy-mysql:
	docker stack deploy --with-registry-auth -c mysql.yml mysql

deploy-rabbitmq:
	docker stack deploy --with-registry-auth -c rabbitmq.yml rabbitmq

deploy-crawler:
	docker stack deploy --with-registry-auth -c financialdata/crawler.yml financialdata

deploy-crawler-scheduler:
	docker stack deploy --with-registry-auth -c financialdata/scheduler.yml financialdata

deploy-api:
	docker stack deploy --with-registry-auth -c api/api.yml api
