# FinMindBook 14.3.5 - 部署 Traefik 與 API

本節在前面的基礎上，加入 traefik 與 api，
由 traefik 作為反向代理（reverse proxy），
負責 http/https 導向、SSL 憑證（Let's Encrypt）與 loading balance，
對外提供 FinMind API 服務。

- traefik：反向代理（http 80、https 443、dashboard 8889、metrics 8082）
- api：FinMind API，由 traefik 依 Host / Path 規則導流

## 設定 node label
延續前面小節的 label，並加上 api 所需的 node label。

    docker node update --label-add api=true <node>

## 建立 traefik network
api 與 traefik 透過 traefik-public 這個 overlay network 溝通，需先建立。

    docker network create --driver=overlay traefik-public

## build、push image
    make create-grafana-docker-image
    make create-prometheus-docker-image
    make create-rabbitmq-docker-image
    make create-airflow-docker-image
    make push-grafana-docker-image
    make push-prometheus-docker-image
    make push-rabbitmq-docker-image
    make push-airflow-docker-image

## 部署前面的服務
    make deploy-grafana-prometheus
    make deploy-netdata
    make deploy-mysql
    make deploy-rabbitmq
    make deploy-crawler3
    make deploy-airflow

## 部署 traefik
    make deploy-traefik
    # docker stack deploy -c traefik.yml tr

## 部署 api
    make deploy-api
    # docker stack deploy -c api.yml api
