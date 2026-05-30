# FinMindBook 14.2.2 - Grafana + Prometheus

本節用 docker compose 同時啟動 grafana 與 prometheus，
由 prometheus 收集 metrics，再用 grafana 視覺化成 dashboard。

## 啟動 grafana、prometheus
    docker compose -f grafana_prometheus.yml up -d

- prometheus：http://localhost:9090
- grafana：http://localhost:3000（帳號 admin，密碼 pass）
