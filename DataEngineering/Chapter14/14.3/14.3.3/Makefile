# image
create-grafana-docker-image:
	docker build --no-cache -f grafana/Dockerfile -t linsamtw/grafana:14.3.3 .

create-prometheus-docker-image:
	docker build --no-cache -f prometheus/Dockerfile -t linsamtw/prometheus:14.3.3 .

create-rabbitmq-docker-image:
	docker build --no-cache -f rabbitmq/Dockerfile -t linsamtw/rabbitmq:14.3.3 .

# push
push-grafana-docker-image:
	docker push linsamtw/grafana:14.3.3

push-prometheus-docker-image:
	docker push linsamtw/prometheus:14.3.3

push-rabbitmq-docker-image:
	docker push linsamtw/rabbitmq:14.3.3

# deploy
deploy-grafana-prometheus:
	docker stack deploy -c grafana_prometheus.yml monitor

deploy-netdata:
	docker stack deploy -c netdata.yml netdata

deploy-mysql:
	docker stack deploy -c mysql.yml mysql

deploy-rabbitmq:
	docker stack deploy -c rabbitmq.yml rabbitmq

deploy-crawler:
	docker stack deploy -c crawler.yml crawler
