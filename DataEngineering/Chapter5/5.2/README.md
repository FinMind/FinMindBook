# FinMindBook 5.2 - 撰寫台股爬蟲

本節撰寫證交所（twse）、櫃買中心（tpex）、期交所（taifex）三支爬蟲，
爬取資料後做清理、schema 檢查，並先暫存為 csv（下一節再上傳資料庫）。
爬蟲進入點皆接收 start_date、end_date 兩個參數。

## 安裝套件
    uv sync

## 爬取證交所股價
    uv run python src/twse_crawler.py 2021-04-01 2021-04-12

## 爬取櫃買中心股價
    uv run python src/tpex_crawler.py 2021-04-01 2021-04-12

## 爬取期交所期貨
    uv run python src/taifex_crawler.py 2021-04-01 2021-04-12
