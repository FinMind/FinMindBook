# FinMindBook 14.2 - 單機監控

本節在單機上用 docker compose 啟動監控服務，
與 14.3 用 Docker Swarm 部署的差異在於：本節以
`docker compose -f xxx.yml up -d` 啟動，適合單機測試與學習。

## 各小節說明
- 14.2.1：啟動 prometheus，收集 metrics（port 9090）
- 14.2.2：同時啟動 grafana 與 prometheus，將 metrics 視覺化（port 3000）
- 14.2.3：啟動 netdata，監控機器硬體資源（port 19999）
