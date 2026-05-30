# FinMindBook 7.2.2 - FastAPI 查詢服務

以 FastAPI 提供台股資料查詢 API，從 MySQL 讀取爬蟲落地的資料。

## install python env
    uv sync

## gen env variable
    python genenv.py

## run local
    uv run --env-file=.env uvicorn api.main:app --reload --port 8888

## build docker
    docker build -f Dockerfile -t api3:7.2.2 .

## up api
    docker compose -f api.yml up
