from celery import Celery

app = Celery(
    "task",
    # 只包含 tasks.py 裡面的程式, 才會成功執行
    include=["tasks"],
    # 連線到 redis,
    broker="redis://localhost:6379/0",
)
