# FinMindBook 7.6 financialdata - crawler image 與 swarm service

爬蟲服務（Celery worker、scheduler）的程式與部署設定。
本機可用 docker compose 測試，正式環境由上層 7.6/Makefile 以 docker stack 部署。指令詳見 Makefile。

## install python env
    uv sync

## build & push image
    docker build -f Dockerfile -t crawler3:7.2.1 .
    docker tag crawler3:7.2.1 linsamtw/crawler3:7.2.1
    docker push linsamtw/crawler3:7.2.1

## run celery (local)
    uv run --env-file=.env celery -A financialdata.tasks.worker worker --loglevel=info --concurrency=1 --hostname=%h -Q twse
    uv run --env-file=.env celery -A financialdata.tasks.worker worker --loglevel=info --concurrency=1 --hostname=%h -Q tpex

## up crawler (local compose)
    docker compose -f crawler.yml up
    docker compose -f scheduler.yml up

## send task
    uv run --env-file=.env python -m financialdata.producer taiwan_stock_price 2021-04-01 2021-04-12
