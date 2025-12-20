FROM ubuntu:22.04

# 系統升級、安裝 uv
RUN apt-get update && apt-get install -y curl && curl -LsSf https://astral.sh/uv/install.sh | sh

RUN mkdir /FinMindProject
COPY . /FinMindProject/
WORKDIR /FinMindProject/

# env
ENV PATH="/root/.local/bin/:$PATH"
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# install package
RUN uv sync

# genenv
RUN VERSION=RELEASE uv run python genenv.py
 
# 預設執行的指令
CMD ["uv", "run", "--env-file=.env", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8888"]
