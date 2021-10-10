import pymysql
import pandas as pd
import io
import sys
from loguru import logger
from sqlalchemy import (
    create_engine,
    engine,
)
import requests


def get_mysql_financialdata_conn() -> engine.base.Connection:
    address = f"mysql+pymysql://root:test@139.162.104.54:3306/FinancialData"
    engine = create_engine(address)
    connect = engine.connect()
    return connect


def read_sql_file(table: str) -> str:
    fd = open(f"./sql/{table}.sql", "r")
    sql = fd.read()
    fd.close()
    return sql


def create_table(
    table: str,
    mysql_conn: engine.base.Connection,
):
    sql = read_sql_file(table)
    try:
        logger.info(
            f"create table {table}"
        )
        mysql_conn.execute(sql)
    except:
        logger.info(
            f"{table} already exists"
        )


def download_data(
    table: str,
    mysql_conn: engine.base.Connection,
):
    logger.info("download data")
    url = f"https://github.com/FinMind/FinMindBook/releases/download/data/{table}.csv"
    resp = requests.get(url)
    df = pd.read_csv(
        io.StringIO(
            resp.content.decode("utf-8")
        )
    )
    try:
        logger.info("upload to mysql")
        df.to_sql(
            name=table,
            con=mysql_conn,
            if_exists="append",
            index=False,
            chunksize=1000,
        )
    except:
        logger.info("already upload")


def main(table: str):
    mysql_conn = (
        get_mysql_financialdata_conn()
    )
    create_table(
        table=table,
        mysql_conn=mysql_conn,
    )
    download_data(
        table=table,
        mysql_conn=mysql_conn,
    )


if __name__ == "__main__":
    table = sys.argv[1]
    main(table)
