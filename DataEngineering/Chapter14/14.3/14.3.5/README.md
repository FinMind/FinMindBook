# traefik

## create network
    docker network create --driver=overlay traefik-public

## deploy:
	docker stack deploy -c traefik.yml tr

