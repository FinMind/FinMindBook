# FinMindBook

## run docker
    docker run -it --rm continuumio/miniconda3:4.3.27 bash

## build docker
    docker build -f Dockerfile -t crawler:dev .

## create docker network
    docker network create my_network

## up mysql, rabbitmq
    docker-compose -f rabbitmq.yml up -d
    docker-compose -f mysql.yml up -d

## up celery
    docker-compose -f crawler.yml up

## up multi celery
    docker-compose -f crawler_multi_celery.yml up
