# FinMindBook 5.5 - RabbitMQ + Celery 分散式爬蟲

本節引入 RabbitMQ 作為 message queue、Celery 作為任務佇列，
將爬蟲任務由 producer 發送、worker 接收執行，達成分散式爬蟲。

## 內容
    5.5.2 部署 RabbitMQ（含 flower 監控）
    5.5.3 Celery producer / worker 入門
    5.5.4 指定 queue 路由任務
    5.5.5 整合爬蟲、MySQL、RabbitMQ、Celery 的完整專案
