import copy
import importlib
import os
import typing
import uuid

import numpy as np
import pandas as pd
from loguru import logger
from sqlalchemy import engine
from tqdm import tqdm

from financialdata.backend import db
from financialdata.backend.db.data_db_mapping import (
    DDB_ID_KEY_DICT,
    DDB_TABLE,
    DDB_TABLE_VERSION,
    FILTER_ID_KEY_DICT,
    FILTER_LAST_DATE,
    IS_UPDATE_DDB,
    NOT_FILTER_DATA,
    UPLOAD_DDB_ID_TABLE,
    IS_UPDATE_MySQL,
)
from financialdata.backend.db.router import Router
from financialdata.Log import Status
from financialdata.schema.dataset import check_schema
from financialdata.Tasks.Worker import CallbackTask, app



def upload_data(df: pd.DataFrame, dataset: str, db_router: Router):
    ddb_table = DDB_TABLE.get(dataset, "")
    ddb_table_version = DDB_TABLE_VERSION.get(dataset, "")
    upload_ddb_id_table = UPLOAD_DDB_ID_TABLE.get(dataset, True)
    data_id_key = FILTER_ID_KEY_DICT.get(dataset, "")
    if FILTER_LAST_DATE.get(dataset, False):
        data_id = df[data_id_key].values[0]
        last_date = get_last_date_from_ddb(
            db_router.ddb_conn,
            ddb_table,
            ddb_table_version,
            upload_ddb_id_table,
            data_id_key,
            data_id,
        )
        df = df[df["date"] > last_date]
    if IS_UPDATE_MySQL.get(dataset, True):
        mysql_table = db.data_db_mapping.MYSQL_TABLE.get(dataset)
        mysql_conn = get_conn(dataset, db_router)
        db.upload_data(
            df=df, table=mysql_table, mysql_conn=mysql_conn,
        )
    if IS_UPDATE_DDB.get(dataset, False):
        if NOT_FILTER_DATA.get(dataset, False):
            pass
        else:
            df = filter_data(df.copy(), ddb_table=ddb_table)
        db.upload_data(
            df=df,
            table=ddb_table,
            ddb_sess=db_router.ddb_conn,
            upload_ddb_id_table=upload_ddb_id_table,
            ddb_table_version=ddb_table_version,
        )


@app.task(base=CallbackTask)
def crawler_history(
    dataset: str,
    parameter: typing.Dict[str, typing.Union[str, int, float]],
    queue: str = "",
):
    name = dataset
    last_date = "2000-01-01"
    df = getattr(
        importlib.import_module(f"financialdata.Crawler.{dataset}"), "crawler",
    )(parameter=parameter, history=True, queue=queue)
    if len(df) > 0:
        df = check_schema(df.copy(), dataset)
        name, last_date = get_log_name_last_date(df, name, last_date)
        upload_data(df, dataset, db.router)

    Status.save_crawler_process(
        conn=db.router.mysql_crawler_log_conn,
        table=db.data_db_mapping.MYSQL_TABLE.get(dataset),
        name=name,
        last_date=last_date,
    )


@app.task(base=CallbackTask)
def create_table(dataset: str):
    sql = getattr(
        importlib.import_module(f"financialdata.Crawler.{dataset}"),
        "create_table",
    )()
    conn = get_conn(dataset, db.router)
    if isinstance(conn, engine.base.Connection):
        db.commit(sql=sql, mysql_conn=conn)


def History(dataset: str):
    mysql_table = db.data_db_mapping.MYSQL_TABLE.get(dataset)
    queue = DATASET_QUEUE.get(dataset, "")
    Status.create_log_table(
        conn=db.router.mysql_crawler_log_conn,
        table=mysql_table,
        last_date_type="date",
    )
    create_table.s(dataset).apply_async(queue=queue[0]) if isinstance(
        queue, list
    ) else create_table.s(dataset).apply_async(queue=queue)
    loop_list = getattr(
        importlib.import_module(f"financialdata.Crawler.{dataset}"),
        "create_loop_list",
    )(db_router=db.router, history=True)
    for loop in tqdm(loop_list):
        if isinstance(queue, list):
            for q in queue:
                crawler_history.s(dataset, loop, q).apply_async(queue=q)
        else:
            crawler_history.s(dataset, loop, queue).apply_async(queue=queue)


@app.task(base=CallbackTask)
def crawler_new(
    dataset: str,
    parameter: typing.Dict[str, typing.Union[str, int, float]],
    queue: str,
):
    name = dataset
    last_date = "2000-01-01"
    df = getattr(
        importlib.import_module(f"financialdata.Crawler.{dataset}"), "crawler",
    )(parameter=parameter, history=False, queue=queue)
    if len(df) > 0:
        df = check_schema(df.copy(), dataset)
        name, last_date = get_log_name_last_date(df, name, last_date)
        upload_data(df, dataset, db.router)

    Status.save_crawler_process(
        conn=db.router.mysql_crawler_log_conn,
        table=db.data_db_mapping.MYSQL_TABLE.get(dataset),
        name=name,
        last_date=last_date,
        parameter=parameter,
    )


def queue_in_mq(
    queue_parm: typing.Tuple[
        str, typing.Dict[str, typing.Union[str, int, float]]
    ],
    queue_list: typing.List[str],
):
    return queue_parm in queue_list


def Update(dataset: str):
    parameter_list = getattr(
        importlib.import_module(f"financialdata.Crawler.{dataset}"),
        "create_loop_list",
    )(db_router=db.router, history=False)
    queue = DATASET_QUEUE.get(dataset, "")
    queue_list = get_message_queue_list(queue)
    for parameter in tqdm(parameter_list):
        if isinstance(queue, list):
            for q in queue:
                if queue_in_mq(
                    queue_parm=(dataset, parameter, q), queue_list=queue_list,
                ):
                    continue
                else:
                    crawler_new.s(dataset, parameter, q).apply_async(queue=q)
        else:
            if queue_in_mq(
                queue_parm=(dataset, parameter, queue), queue_list=queue_list,
            ):
                continue
            else:
                crawler_new.s(dataset, parameter, queue).apply_async(
                    queue=queue
                )
