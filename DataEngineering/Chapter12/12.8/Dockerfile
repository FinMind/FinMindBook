FROM continuumio/miniconda3:4.7.12

RUN mkdir /FinMindProject
COPY . /FinMindProject/
COPY ./airflow.cfg /FinMindProject/dataflow/airflow.cfg
WORKDIR /FinMindProject/

# airflow
ARG AIRFLOW_USER_HOME=/FinMindProject/dataflow
ARG AIRFLOW_DEPS=""
ARG PYTHON_DEPS=""
ENV AIRFLOW_HOME=${AIRFLOW_USER_HOME}

# install package
RUN pip install pipenv==2020.6.2 && pipenv sync

WORKDIR /FinMindProject/
