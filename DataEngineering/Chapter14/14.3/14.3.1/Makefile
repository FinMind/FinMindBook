# image
create-grafana-docker-image:
	docker build -f grafana/Dockerfile -t linsamtw/grafana:14.3.1 .

create-prometheus-docker-image:
	docker build -f prometheus/Dockerfile -t linsamtw/prometheus:14.3.1 .

# deploy
deploy-grafana-prometheus:
	docker stack deploy -c grafana_prometheus.yml monitor

deploy-netdata:
	docker stack deploy -c netdata.yml netdata

