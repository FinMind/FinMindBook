FROM continuumio/miniconda3:4.3.27

RUN apt-get update

RUN mkdir /FinMindProject
COPY . /FinMindProject/
WORKDIR /FinMindProject/

# install package
RUN pip install pipenv==2020.6.2 && pipenv sync

# genenv
RUN VERSION=RELEASE python genenv.py
