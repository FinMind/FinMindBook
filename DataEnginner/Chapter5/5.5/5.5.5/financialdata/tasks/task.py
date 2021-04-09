import importlib
import typing

from loguru import logger

from financialdata.backend import db
from financialdata.tasks.worker import app


# 註冊 task, 有註冊的 task 才可以變成任務發送給 rabbitmq
@app.task()
def crawler(dataset: str, parameter: typing.Dict[str, str]):
    # 使用 getattr, importlib, 根據不同 dataset, 使用相對應的 crawler 收集資料
    df = getattr(
        importlib.import_module(f"financialdata.crawler.{dataset}"),
        "crawler",
    )(parameter=parameter)
    db.upload_data(df, dataset, db.router.mysql_financialdata_conn)


def Update(dataset: str, start_date: str, end_date: str):
    parameter_list = getattr(
        importlib.import_module(f"financialdata.crawler.{dataset}"),
        "gen_task_paramter_list",
    )(start_date=start_date, end_date=end_date)
    for parameter in parameter_list:
        logger.info(f"{dataset}, {parameter}")
        # crawler.s(dataset, parameter).apply_async()
