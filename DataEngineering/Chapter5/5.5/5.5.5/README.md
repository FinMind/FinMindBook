# FinMindBook 5.5.5 - 整合爬蟲、MySQL、RabbitMQ、Celery

本節整合前面所有元件，成為完整的分散式爬蟲專案：
producer 依資料來源（twse、tpex）將任務發送到對應 queue，worker 分別消化各自的 queue。
指令對應 Makefile 的 target。

## 安裝套件
    make install-python-env
    # uv sync

## 部署 mysql
    make create-mysql
    # docker compose -f mysql.yml up -d

## 部署 rabbitmq
    make create-rabbitmq
    # docker compose -f rabbitmq.yml up -d

## 建立環境變數
    make gen-dev-env-variable
    # python genenv.py

## 啟動 worker（twse queue）
    make run-celery-twse
    # uv run celery -A financialdata.tasks.worker worker --loglevel=info --concurrency=1 --hostname=%h -Q twse

## 啟動 worker（tpex queue）
    make run-celery-tpex
    # uv run celery -A financialdata.tasks.worker worker --loglevel=info --concurrency=1 --hostname=%h -Q tpex

## 發送爬蟲任務
    make sent-taiwan-stock-price-task
    # uv run python -m financialdata.producer taiwan_stock_price 2021-04-01 2021-04-12
