# FinMindBook 8.1.4 - 爬蟲測試與 Docker 部署

替爬蟲專案撰寫 pytest 測試並量測覆蓋率，再透過 Docker 打包、推送與部署。指令皆對應 Makefile target。

## install package
    # make install-python-env
    uv sync

## gen env variable
    # make gen-dev-env-variable
    python genenv.py

## run test with coverage
    # make test-cov
    uv run --env-file=.env pytest --cov-report term-missing --cov-config=.coveragerc --cov=./financialdata/ tests/

## build & push image
    # make build-image
    docker build -f Dockerfile -t crawler3:7.2.1 .
    # make tag-image
    docker tag crawler3:7.2.1 linsamtw/crawler3:7.2.1
    # make push-image
    docker push linsamtw/crawler3:7.2.1

## start service

### network & mysql volume
    # make create-network
    docker network create my_network
    # make create-mysql-volume
    docker volume create mysql

### mysql / rabbitmq
    # make create-mysql
    docker compose -f mysql.yml up -d
    # make create-rabbitmq
    docker compose -f rabbitmq.yml up -d

### crawler / scheduler
    # make up-crawler3
    docker compose -f crawler.yml up
    # make up-scheduler
    docker compose -f scheduler.yml up
