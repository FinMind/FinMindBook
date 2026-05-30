# FinMindBook 5.6.2 - APScheduler 入門

本節用 APScheduler 的 BackgroundScheduler，以類似 crontab 的設定定時觸發任務
（範例為每 5 秒執行一次 sent_crawler_task）。指令對應 Makefile 的 target。

## 安裝套件
    uv sync

## 啟動排程器
    make run-scheduler
    # uv run python scheduler.py
