# FinMindBook 14.3.4 - Airflow

本目錄為 airflow 子專案，內含 DAG、ETL 與部署設定，
用來在 Docker Swarm 上排程派發爬蟲任務。

- Dockerfile：以 ubuntu 22.04 為基底，用 uv 安裝依賴並打包成 image
- airflow.yml：swarm deploy 檔，包含 initdb、create-user、redis、
  webserver、flower、scheduler、worker 與爬蟲 worker（crawler_twse、crawler_tpex）
- dataflow/：DAG 與 ETL 程式

## build、push image
於上層 14.3.4 目錄執行：

    make create-airflow-docker-image
    # docker build --no-cache -f Dockerfile -t linsamtw/dataflow3:14.3.4 .
    make push-airflow-docker-image
    # docker push linsamtw/dataflow3:14.3.4

## 部署 airflow
於上層 14.3.4 目錄執行：

    make deploy-airflow
    # docker stack deploy -c airflow/airflow.yml airflow

部署後可在瀏覽器開啟：

- airflow webserver：http://localhost:8888（帳號 admin，密碼 admin）
- flower：http://localhost:5556
