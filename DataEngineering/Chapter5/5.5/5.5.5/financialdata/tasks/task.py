import importlib
import typing

from financialdata.backend import db
from financialdata.tasks.worker import app


# 註冊 task, 有註冊的 task 才可以變成任務發送給 rabbitmq
@app.task()
def crawler(dataset: str, parameter: typing.Dict[str, str]):
    # 使用 getattr, importlib,
    # 根據不同 dataset, 使用相對應的 crawler 收集資料
    # 爬蟲
    df = getattr(
        importlib.import_module(f"financialdata.crawler.{dataset}"),
        "crawler",
    )(parameter=parameter)
    # 上傳資料庫
    db.upload_data(df, dataset, db.router.mysql_financialdata_conn)
