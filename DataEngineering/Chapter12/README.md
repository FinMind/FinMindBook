# FinMindBook Chapter12 - Airflow 排程與 Docker Swarm 部署

本章用 Airflow 排程定時派發爬蟲任務，並透過 Docker Swarm 部署整套服務。
各小節循序漸進：12.5 部署基礎 Airflow，12.7 介紹各種 Operator（含 DockerOperator），12.8 加入環境變數管理與正式站部署流程。

## 初始化 swarm
    make swarm-init
    # docker swarm init

## 建立 swarm overlay network
    make create-swarm-network
    # docker network create --scope=swarm --driver=overlay my_network

## 部署 portainer
    make create-portainer
    # docker stack deploy -c portainer.yml portainer
