# FinMindBook 10.5 - FastAPI 服務

提供 taiwan_stock_price API，從 MySQL 查詢台股股價，並以 docker swarm 搭配 traefik 部署。

## install
    make install-python-env

## gen env variable
    make gen-dev-env-variable

## run
    uv run uvicorn main:app --reload --port 8888

## test
    make test-cov

## build image
    make build-image

## push image
    make push-image

## up
    make up-api

## deploy
    make deploy
