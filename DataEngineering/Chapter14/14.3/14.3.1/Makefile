# image
create-grafana-docker-image:
	docker build --no-cache -f grafana/Dockerfile -t linsamtw/grafana:14.3.1 .

create-prometheus-docker-image:
	docker build --no-cache -f prometheus/Dockerfile -t linsamtw/prometheus:14.3.1 .

# push
push-grafana-docker-image:
	docker push linsamtw/grafana:14.3.1

push-prometheus-docker-image:
	docker push linsamtw/prometheus:14.3.1

# deploy
deploy-grafana-prometheus:
	docker stack deploy -c grafana_prometheus.yml monitor

deploy-netdata:
	docker stack deploy -c netdata.yml netdata

