# FinMindBook 14.3.3 - 部署 RabbitMQ 與 Crawler

本節在前面的基礎上，加入 rabbitmq 與爬蟲，
完成「派發任務 → 排隊 → 爬蟲消化」的分散式爬蟲架構。

- rabbitmq：任務佇列（port 5672、management 15672、metrics 15692）
- crawler_twse：消化 twse queue 的爬蟲
- crawler_tpex：消化 tpex queue 的爬蟲
- sent_task：派發爬蟲任務（producer）

## 設定 node label
    docker node update --label-add grafana=true <node>
    docker node update --label-add manager=true <node>
    docker node update --label-add mysql=true <node>
    docker node update --label-add rabbitmq=true <node>
    docker node update --label-add crawler_twse=true <node>
    docker node update --label-add crawler_tpex=true <node>
    docker node update --label-add sent_task=true <node>

## build、push image
    make create-grafana-docker-image
    make create-prometheus-docker-image
    make create-rabbitmq-docker-image
    make push-grafana-docker-image
    make push-prometheus-docker-image
    make push-rabbitmq-docker-image

## 部署監控與資料庫
    make deploy-grafana-prometheus
    make deploy-netdata
    make deploy-mysql

## 部署 rabbitmq
    make deploy-rabbitmq
    # docker stack deploy -c rabbitmq.yml rabbitmq

## 部署 crawler
    make deploy-crawler3
    # docker stack deploy -c crawler.yml crawler
