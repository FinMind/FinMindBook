
create-mysql-volume:
	docker volume create mysql

create-network:
	docker network create my_network

deploy-mysql:
	docker stack deploy --with-registry-auth -c mysql.yml mysql

deploy-rabbitmq:
	docker stack deploy --with-registry-auth -c rabbitmq.yml rabbitmq


