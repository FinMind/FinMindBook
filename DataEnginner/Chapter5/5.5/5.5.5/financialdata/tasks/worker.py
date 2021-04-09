from celery import Celery
from financialdata.config import (
    WORKER_ACCOUNT,
    WORKER_PASSWORD,
    MESSAGE_QUEUE_HOST,
    MESSAGE_QUEUE_PORT,
)

app = Celery(
    "task",
    # 只包含 Tasks.py 裡面的程式, 才會成功執行
    include=["financialdata.tasks.task"],
    # 連線到 rabbitmq,
    # pyamqp://user:password@rabbitmq_ip:5672/
    # 這裡我們帳號密碼都是 worker
    # broker="pyamqp://worker:worker@rabbitmq_ip:5672/",
    broker=f"pyamqp://{WORKER_ACCOUNT}:{WORKER_PASSWORD}@{MESSAGE_QUEUE_HOST}:{MESSAGE_QUEUE_PORT}/",
)
