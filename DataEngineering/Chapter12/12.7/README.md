# FinMindBook 12.7 - Airflow Operator 與 DockerOperator

本節在 12.5 部署的基礎上，介紹 Airflow 各種 Operator（Dummy、Bash、Python、BranchPython、Docker）。
其中 DockerOperator 會在每次執行時 pull 最新 image 並另開容器跑爬蟲，因此 scheduler 需掛載 docker.sock。

## build image
    make build-image
    # docker build --no-cache -f Dockerfile -t linsamtw/dataflow3:12.7 .
    make push-image
    # docker push linsamtw/dataflow3:12.7

## build cache image
    make build-cache-image
    # docker build --no-cache -f Dockerfile.cache -t linsamtw/dataflow3:12.7 .

## 部署 airflow（DockerOperator 版本）
本版 airflow-docker-operator.yml 的 scheduler 額外掛載 /var/run/docker.sock，讓 DockerOperator 能在宿主機啟動容器。

    docker stack deploy -c airflow-docker-operator.yml airflow

## 部署一般 airflow
    make create-airflow
    # docker stack deploy -c airflow.yml airflow
