# FinMindBook 5.3 - 部署 MySQL 資料庫

本節用 docker compose 部署資料庫，作為後續存放台股資料的地方。

- mysql：資料庫（port 3306）
- phpmyadmin：mysql 視覺化管理介面（port 8000）

## 建立 mysql volume
    docker volume create mysql

## 部署 mysql
    docker compose -f mysql.yml up -d
