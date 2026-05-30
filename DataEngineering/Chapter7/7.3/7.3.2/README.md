# FinMindBook 7.3.2 - 建立 Docker Swarm 叢集

說明如何初始化 manager 並讓 worker 節點加入 swarm（本節為說明性質，無可執行檔案）。

## init swarm manager
    docker swarm init

## join as worker
    docker swarm join --token <token> <manager-ip>:2377
