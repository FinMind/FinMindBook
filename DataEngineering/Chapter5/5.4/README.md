# FinMindBook 5.4 - 將爬蟲資料上傳資料庫

本節在 5.2 爬蟲的基礎上，加入資料庫連線（financialdata/clients.py、router.py），
將清理後的資料以 to_sql 上傳 MySQL 的 financialdata 資料庫。

## 安裝套件
    uv sync

## 建立資料表
    # 於 phpmyadmin 或 mysql client 執行
    # create_table.sql            一般資料表
    # create_partition_table.sql  依年份 partition 的資料表

## 爬取並上傳證交所股價
    uv run python financialdata/twse_crawler.py 2021-04-01 2021-04-12

## 爬取並上傳櫃買中心股價
    uv run python financialdata/tpex_crawler.py 2021-04-01 2021-04-12

## 爬取並上傳期交所期貨
    uv run python financialdata/taifex_crawler.py 2021-04-01 2021-04-12
