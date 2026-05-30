# FinMindBook Chapter7 - 爬蟲系統部署與 Docker Swarm

本章以台股爬蟲為例，將 Celery、RabbitMQ、MySQL、FastAPI 等服務容器化，
並從單機 docker compose 進階到 Docker Swarm + Portainer 的多機叢集部署。

## 各節主題
- 7.2 容器化 crawler / API，以 docker compose 啟動 Celery、RabbitMQ、MySQL
- 7.3 Docker Swarm 介紹
- 7.5 Portainer 叢集管理介面
- 7.6 以 Docker Swarm 部署完整爬蟲系統
