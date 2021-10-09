FROM continuumio/miniconda3:4.3.27

RUN apt-get update

RUN mkdir /FinMindProject
COPY . /FinMindProject/
WORKDIR /FinMindProject/

# install package
RUN pip install pipenv && pipenv sync

# genenv
RUN VERSION=RELEASE python genenv.py
