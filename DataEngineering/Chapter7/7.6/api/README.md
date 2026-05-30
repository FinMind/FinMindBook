# FinMindBook 7.6 api - API image 與 swarm service

FastAPI 查詢服務的程式與部署設定。
本機可用 docker compose 測試，正式環境以 docker stack 部署到 swarm。指令詳見 Makefile。

## install python env
    uv sync

## run local
    uv run --env-file=.env uvicorn api.main:app --reload --port 8888

## build & push image
    docker build -f Dockerfile -t api3:7.2.2 .
    docker tag api3:7.2.2 linsamtw/api3:7.2.2
    docker push linsamtw/api3:7.2.2

## deploy to swarm
    docker stack deploy -c api.yml api
