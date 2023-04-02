FROM continuumio/miniconda3:4.9.2

RUN mkdir /FinMindProject
COPY . /FinMindProject/
COPY ./airflow.cfg /FinMindProject/dataflow/airflow.cfg
WORKDIR /FinMindProject/

# install package
RUN pip install pipenv==2020.6.2 && pipenv sync

WORKDIR /FinMindProject/
