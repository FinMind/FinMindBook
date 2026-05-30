# FinMindBook 12.8 - 環境變數管理與正式站部署

本節相較前幾節，加入用 genenv.py 從 local.ini 依環境（dev / staging / release）產生 .env，
讓 airflow.yml 以 `uv run --env-file=.env` 帶入 MySQL 連線等設定，並用 Celery + Redis 多 queue 部署正式站。

## 產生環境變數
local.ini 內分 DEFAULT(dev)、STAGING、RELEASE 三區，genenv.py 依 VERSION 或 hostname 選擇對應區段寫入 .env。

    make gen-dev-env-variable
    # python genenv.py
    make gen-staging-env-variable
    # VERSION=STAGING python genenv.py
    make gen-release-env-variable
    # VERSION=RELEASE python genenv.py

## build image
    make build-image
    # docker build --no-cache -f Dockerfile -t linsamtw/dataflow3:12.8 .
    make build-cache-image
    # docker build --no-cache -f Dockerfile.cache -t linsamtw/dataflow3:12.8 .
    make push-image
    # docker push linsamtw/dataflow3:12.8

## 部署 airflow
    make create-airflow
    # docker stack deploy -c airflow.yml airflow

## 移除 airflow
    make rm-airflow
    # docker stack rm airflow

## 一鍵更新正式站
依序執行：移除 airflow、產生 release 環境變數、build cache image、push、重新部署。

    make update-airflow
    # rm-airflow gen-release-env-variable build-cache-image push-image create-airflow
