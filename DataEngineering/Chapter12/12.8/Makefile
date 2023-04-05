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

rm-airflow:
	docker stack rm airflow

# 建立 dev 環境變數
gen-dev-env-variable:
	python genenv.py

# 建立 staging 環境變數
gen-staging-env-variable:
	VERSION=STAGING python genenv.py

# 建立 release 環境變數
gen-release-env-variable:
	VERSION=RELEASE python genenv.py

update-airflow: rm-airflow gen-release-env-variable build-cache-image push-image create-airflow
