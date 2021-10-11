from celery import Celery

app = Celery(
    "task",
    # 只包含 tasks.py 裡面的程式, 才會成功執行
    include=["tasks"],
    # 連線到 rabbitmq,
    # pyamqp://user:password@localhost:5672/
    # 本書的帳號密碼都是 worker
    broker="pyamqp://worker:worker@localhost:5672/",
)
