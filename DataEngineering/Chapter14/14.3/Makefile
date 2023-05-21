# init
swarm-init:
	docker swarm init

create-portainer:
	docker stack deploy -c portainer.yml portainer

create-swarm-network:
	docker network create --scope=swarm --driver=overlay my_network
