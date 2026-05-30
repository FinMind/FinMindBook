# FinMindBook 7.2 - 容器化 crawler 與 API

將爬蟲（Celery worker）與 FastAPI 服務打包成 Docker image，
並以 docker compose 啟動 RabbitMQ、MySQL 及各服務。

## 各節主題
- 7.2.1 crawler：Celery + RabbitMQ + MySQL，發送與消化爬蟲任務
- 7.2.2 api：FastAPI 查詢已落地的台股資料
