# 由於 continuumio/miniconda3:4.3.27 中的 Debian
# 版本太舊，因此改用 ubuntu 系統
FROM ubuntu:18.04

# 系統升級、安裝 python
RUN apt-get update && apt-get install python3.7 -y && apt-get install python3-pip -y

RUN mkdir /FinMindProject
COPY ./airflow /FinMindProject/
COPY ./airflow/airflow.cfg /FinMindProject/dataflow/airflow.cfg
WORKDIR /FinMindProject/

# env
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# install package
RUN pip3 install pipenv==2020.6.2
RUN pipenv sync

# airflow
ARG AIRFLOW_USER_HOME=/FinMindProject/dataflow
ARG AIRFLOW_DEPS=""
ARG PYTHON_DEPS=""
ENV AIRFLOW_HOME=${AIRFLOW_USER_HOME}

WORKDIR /FinMindProject/
