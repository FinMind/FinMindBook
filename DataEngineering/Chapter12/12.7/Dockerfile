FROM ubuntu:22.04

# 系統升級、安裝 uv
RUN apt-get update && apt-get install -y curl && curl -LsSf https://astral.sh/uv/install.sh | sh

RUN mkdir /FinMindProject
COPY . /FinMindProject/
COPY ./airflow.cfg /FinMindProject/dataflow/airflow.cfg
WORKDIR /FinMindProject/

# env
ENV PATH="/root/.local/bin/:$PATH"
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# install package
RUN uv sync

# airflow
ARG AIRFLOW_USER_HOME=/FinMindProject/dataflow
ARG AIRFLOW_DEPS=""
ARG PYTHON_DEPS=""
ENV AIRFLOW_HOME=${AIRFLOW_USER_HOME}

WORKDIR /FinMindProject/
