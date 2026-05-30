# FinMindBook 7.5.3 - 部署 Portainer

於 Docker Swarm 中以 stack 部署 Portainer（agent + portainer-ce），
完成後可由瀏覽器 9000 port 進入管理介面。

## deploy portainer
    docker stack deploy -c portainer.yml por
