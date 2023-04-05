swarm-init:
	docker swarm init

create-portainer:
	docker stack deploy -c portainer.yml portainer

create-network:
	docker network create --scope=swarm --driver=overlay my_network

create-mysql-volume:
	docker volume create mysql

create-mysql:
	docker stack deploy -c mysql.yml mysql

build-image:
	docker build --no-cache -f Dockerfile -t linsamtw/dataflow:12.8 .

push-image:
	docker push linsamtw/dataflow:12.8

build-cache-image:
	docker build --no-cache -f Dockerfile.cache -t linsamtw/dataflow:12.8 .

create-airflow:
	docker stack deploy -c airflow.yml airflow
