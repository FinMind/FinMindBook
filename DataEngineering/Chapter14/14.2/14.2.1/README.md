# FinMindBook 14.2.1 - Prometheus

本節用 docker compose 在單機啟動 prometheus，收集各服務的 metrics。

## 啟動 prometheus
    docker compose -f prometheus.yml up -d

瀏覽器開啟 http://localhost:9090
