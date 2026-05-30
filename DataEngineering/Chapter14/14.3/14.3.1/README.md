# FinMindBook 14.3.1 - Grafana、Prometheus、Netdata 監控

本節在 Docker Swarm 上部署監控系統：

- prometheus：收集各服務的 metrics（port 9090）
- grafana：將 metrics 視覺化（port 3000，密碼 pass）
- netdata：監控每台機器的硬體資源（port 19999）

## 設定 node label
部署檔以 placement constraints 指定服務要跑在哪台機器，
因此需先幫 node 貼上 label。

    docker node update --label-add grafana=true <node>
    docker node update --label-add manager=true <node>

## build image
    make create-grafana-docker-image
    make create-prometheus-docker-image

## push image
    make push-grafana-docker-image
    make push-prometheus-docker-image

## 部署 grafana、prometheus
    make deploy-grafana-prometheus
    # docker stack deploy -c grafana_prometheus.yml monitor

## 部署 netdata
    make deploy-netdata
    # docker stack deploy -c netdata.yml netdata
