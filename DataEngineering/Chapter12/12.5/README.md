# FinMindBook 12.5 - 部署 Airflow

本節用 Docker Swarm 部署一套完整的 Airflow，並用 hello_world DAG 驗證排程能正常運作。

## 初始化 swarm 與 network
    make swarm-init
    # docker swarm init
    make create-network
    # docker network create --scope=swarm --driver=overlay my_network

## 部署 portainer
    make create-portainer
    # docker stack deploy -c portainer.yml portainer

## 部署 mysql
    make create-mysql-volume
    # docker volume create mysql
    make create-mysql
    # docker stack deploy -c mysql.yml mysql

## build image
    make build-image
    # docker build --no-cache -f Dockerfile -t linsamtw/dataflow3:12.5 .
    make push-image
    # docker push linsamtw/dataflow3:12.5

## 部署 airflow
    make create-airflow
    # docker stack deploy -c airflow.yml airflow
