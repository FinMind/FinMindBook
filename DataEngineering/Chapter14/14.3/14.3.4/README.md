# FinMindBook 14.3.4 - 部署 Airflow

本節在前面的基礎上，加入 airflow，
用來排程定時派發爬蟲任務，取代手動執行 producer。

airflow 相關設定與 DAG 放在 airflow/ 目錄下，
deploy 檔為 airflow/airflow.yml。

## 設定 node label
延續 14.3.3 的 label，並加上 airflow 所需的 node label
（詳見 airflow/airflow.yml 的 placement 設定）。

## build、push image
    make create-grafana-docker-image
    make create-prometheus-docker-image
    make create-rabbitmq-docker-image
    make create-airflow-docker-image
    make push-grafana-docker-image
    make push-prometheus-docker-image
    make push-rabbitmq-docker-image
    make push-airflow-docker-image

## 部署監控、資料庫、佇列、爬蟲
    make deploy-grafana-prometheus
    make deploy-netdata
    make deploy-mysql
    make deploy-rabbitmq
    make deploy-crawler3

## 部署 airflow
    make deploy-airflow
    # docker stack deploy -c airflow/airflow.yml airflow
