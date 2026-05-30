# FinMindBook 7.6 - 以 Docker Swarm 部署完整爬蟲系統

於 Docker Swarm 叢集部署整套服務：MySQL、RabbitMQ、crawler（Celery）、scheduler 與 API。
各服務以 node label 約束部署到指定節點。指令詳見 Makefile。

## create overlay network
    docker network create --scope=swarm --driver=overlay my_network

## create mysql volume
    docker volume create mysql

## deploy mysql, rabbitmq
    docker stack deploy --with-registry-auth -c mysql.yml mysql
    docker stack deploy --with-registry-auth -c rabbitmq.yml rabbitmq

## deploy crawler, scheduler
    docker stack deploy --with-registry-auth -c financialdata/crawler.yml financialdata
    docker stack deploy --with-registry-auth -c financialdata/scheduler.yml financialdata

## deploy api
    docker stack deploy --with-registry-auth -c api/api.yml api

## send task
    uv run --env-file=.env python -m financialdata.producer taiwan_stock_price 2021-04-01 2021-04-12
