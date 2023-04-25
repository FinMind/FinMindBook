# 由於 continuumio/miniconda3:4.3.27 中的 Debian
# 版本太舊，因此改用 ubuntu 系統
FROM ubuntu:18.04

# 系統升級、安裝 python
RUN apt-get update && apt-get install python3.6 -y && apt-get install python3-pip -y

RUN mkdir /FinMindProject
COPY . /FinMindProject/
WORKDIR /FinMindProject/

# env
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# install package
RUN pip3 install pipenv==2020.6.2
RUN pipenv sync

# genenv
RUN VERSION=RELEASE python3 genenv.py