
create-mysql-volume:
	docker volume create mysql

create-network:
	docker network create --scope=swarm --driver=overlay my_network

deploy-mysql:
	docker stack deploy --with-registry-auth -c mysql.yml mysql

deploy-rabbitmq:
	docker stack deploy --with-registry-auth -c rabbitmq.yml rabbitmq

deploy-financialdata:
	docker stack deploy --with-registry-auth -c financialdata/crawler.yml financialdata

