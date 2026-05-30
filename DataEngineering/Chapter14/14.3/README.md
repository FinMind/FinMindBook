# FinMindBook 14.3 - Docker Swarm

本節將前面建立的爬蟲、資料庫、監控等服務，從單機的 docker compose
搬到 Docker Swarm 上，以叢集（cluster）的方式部署與管理。

## 初始化 swarm
    make swarm-init
    # docker swarm init

## 建立 swarm overlay network
    make create-swarm-network
    # docker network create --scope=swarm --driver=overlay my_network

## 部署 portainer
portainer 是 Docker Swarm 的視覺化管理介面，部署後可在瀏覽器查看 stack、service、container 狀態。

    make create-portainer
    # docker stack deploy -c portainer.yml portainer

部署後開啟 http://127.0.0.1:9000

## 各小節說明
- 14.3.1：部署 grafana、prometheus、netdata 監控服務
- 14.3.2：部署 mysql
- 14.3.3：部署 rabbitmq 與 crawler 爬蟲
- 14.3.4：部署 airflow
- 14.3.5：部署 traefik 與 api
