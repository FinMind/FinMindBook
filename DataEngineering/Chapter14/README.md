# FinMindBook 14 - 監控

本章介紹如何監控資料工程的各項服務，使用三套常見工具：

- prometheus：收集各服務的 metrics
- grafana：將 metrics 視覺化成 dashboard
- netdata：監控每台機器的硬體資源（CPU、記憶體、磁碟等）

## 各小節說明
- 14.2：在單機用 docker compose 啟動監控服務
- 14.3：在多台機器用 Docker Swarm 叢集部署完整服務

兩者差異在於部署方式：14.2 為單機版，指令以 `docker compose -f xxx.yml up -d`
啟動；14.3 為叢集版，改用 `docker stack deploy` 部署到 swarm。
