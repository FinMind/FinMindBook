# FinMindBook - 資料工程

本書以台股資料為例，從零打造一套完整的資料工程系統：
撰寫爬蟲、建立資料庫、提供 Web API，並逐步將服務容器化、
透過 Docker Swarm 部署成分散式叢集，再加上排程、視覺化與監控。

各章程式碼與操作說明放在對應資料夾，每個小節的 README 都附有可直接執行的指令。

## 章節目錄

| 章節 | 主題 |
| --- | --- |
| [Chapter2](Chapter2) | — |
| [Chapter3](Chapter3) | — |
| [Chapter5](Chapter5) | Python 環境管理、撰寫爬蟲、MySQL 資料庫、RabbitMQ + Celery 分散式爬蟲、APScheduler 排程 |
| [Chapter6](Chapter6) | 以 Flask / FastAPI 建立 Web API，對外提供資料庫中的台股資料 |
| [Chapter7](Chapter7) | 爬蟲與 API 容器化，從 docker compose 進階到 Docker Swarm 與 Portainer 全棧部署 |
| [Chapter8](Chapter8) | pytest 單元測試、測試覆蓋率與 Docker 部署 |
| [Chapter10](Chapter10) | 以 traefik 作為反向代理，部署 API 並處理 SSL 與分流 |
| [Chapter11](Chapter11) | 以 Redash 進行資料視覺化，撰寫查詢 SQL |
| [Chapter12](Chapter12) | Airflow 排程，含各種 Operator（DockerOperator）與多環境變數管理 |
| [Chapter13](Chapter13) | Redis + Celery 任務佇列 |
| [Chapter14](Chapter14) | 系統監控：Prometheus、Grafana、Netdata（單機 compose 與 Swarm 兩種部署） |
