# FinMindBook 11.2 - 部署 Redash

以 docker swarm 部署 Redash，包含 redash、scheduler、worker、postgres、redis、nginx 等 services，作為資料視覺化平台。

## deploy
    make deploy

部署後第一次需建立 table，redash.yml 內的 create_table service 會執行
`python /app/manage.py database create_tables`，完成後可在 portainer 刪除該 service。
