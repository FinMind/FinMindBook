# FinMindBook 14.3.2 - 部署 MySQL

本節在 14.3.1 監控系統的基礎上，加入 mysql 資料庫，
並透過 mysql-exporter 將 mysql 的 metrics 提供給 prometheus 監控。

- mysql：資料庫（port 3306）
- mysql-exporter：輸出 mysql metrics 供 prometheus 收集（port 9104）
- phpmyadmin：mysql 視覺化管理介面（port 8080）

## 設定 node label
    docker node update --label-add grafana=true <node>
    docker node update --label-add manager=true <node>
    docker node update --label-add mysql=true <node>

## 建立 mysql volume
mysql.yml 使用 external volume，需先建立，避免資料隨 container 消失。

    docker volume create mysql

## build、push image
    make create-grafana-docker-image
    make create-prometheus-docker-image
    make push-grafana-docker-image
    make push-prometheus-docker-image

## 部署 grafana、prometheus、netdata
    make deploy-grafana-prometheus
    make deploy-netdata

## 部署 mysql
    make deploy-mysql
    # docker stack deploy -c mysql.yml mysql
