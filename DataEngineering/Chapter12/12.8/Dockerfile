# 使用 Ubuntu 22.04 作為基礎映像
FROM ubuntu:22.04

# 系統更新並安裝 curl，然後透過 curl 安裝 uv (Astral.sh 的包管理工具)
# 之後安裝 tzdata 套件以設定時區
RUN apt-get update &&\
    apt-get install -y curl &&\
    curl -LsSf https://astral.sh/uv/install.sh | sh &&\
    apt-get install -y tzdata

# 建立專案目錄
RUN mkdir /FinMindProject

# 複製整個專案內容到容器內的 /FinMindProject
COPY . /FinMindProject/

# 複製 airflow.cfg 到容器內的 airflow config 路徑
COPY ./airflow.cfg /FinMindProject/dataflow/airflow.cfg

# 設定工作目錄，後續命令會在這個目錄下執行
WORKDIR /FinMindProject/

# 設定環境變數
# PATH：將 uv 安裝的二進位路徑加入 PATH
# LC_ALL、LANG：設定容器語言編碼為 UTF-8
# DEBIAN_FRONTEND：避免安裝套件時互動式提示
# TZ：設定時區為台北
ENV PATH="/root/.local/bin/:$PATH"
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Taipei

# 安裝專案依賴，透過 uv 工具自動同步 requirements
RUN uv sync

# airflow 相關環境變數設定
# AIRFLOW_USER_HOME：Airflow home 目錄
# AIRFLOW_DEPS、PYTHON_DEPS：預留參數，可以用來安裝額外依賴
# PYTHONPATH：將 /FinMindProject 加入 Python 搜尋路徑
# AIRFLOW_HOME：指定 Airflow home 目錄
ARG AIRFLOW_USER_HOME=/FinMindProject/dataflow
ARG AIRFLOW_DEPS=""
ARG PYTHON_DEPS=""
ENV PYTHONPATH=/FinMindProject
ENV AIRFLOW_HOME=${AIRFLOW_USER_HOME}

# genenv
RUN VERSION=RELEASE uv run python genenv.py

# 再次設定工作目錄，確保後續命令在正確目錄下執行
WORKDIR /FinMindProject/
