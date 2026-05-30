# FinMindBook 5.6.3 - 排程器整合分散式爬蟲

本節在 5.5.5 的完整專案上，加入 financialdata/scheduler.py 排程器：
每個交易日（mon-fri）15:00 自動呼叫 producer 的 Update，發送當日台股股價爬蟲任務。
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

## 啟動排程器
    make run-scheduler
    # uv run python scheduler.py
