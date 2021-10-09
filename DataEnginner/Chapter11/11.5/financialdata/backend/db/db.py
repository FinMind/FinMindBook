import typing
import importlib

import pandas as pd
import pymysql
from loguru import logger
from sqlalchemy import engine

from financialdata.backend.db import (
    Router,
)


def upload_data(
    df: pd.DataFrame,
    table: str,
    mysql_conn: engine.base.Connection,
):
    if len(df) > 0:
        try:
            df.to_sql(
                name=table,
                con=mysql_conn,
                if_exists="append",
                index=False,
                chunksize=1000,
            )
            return True
        except Exception as e:
            return False


def build_update_sql(
    colname: typing.List[str],
    value: typing.List[str],
):
    update_sql = ",".join(
        [
            ' `{}` = "{}" '.format(
                colname[i],
                str(value[i]),
            )
            for i in range(len(colname))
            if str(value[i])
        ]
    )
    return update_sql


def commit(
    sql: typing.Union[
        str, typing.List[str]
    ],
    mysql_conn: engine.base.Connection = None,
):
    logger.info("commit")
    try:
        trans = mysql_conn.begin()
        if isinstance(sql, list):
            for s in sql:
                try:
                    mysql_conn.execution_options(
                        autocommit=False
                    ).execute(
                        s
                    )
                except Exception as e:
                    logger.info(e)
                    logger.info(s)
                    break

        elif isinstance(sql, str):
            mysql_conn.execution_options(
                autocommit=False
            ).execute(
                sql
            )
        trans.commit()
    except Exception as e:
        trans.rollback()
        logger.info(e)


def build_df_update_sql(
    table: str, df: pd.DataFrame
) -> typing.List[str]:
    logger.info("build_df_update_sql")
    df_columns = list(df.columns)
    sql_list = []
    for i in range(len(df)):
        temp = list(df.iloc[i])
        value = [
            pymysql.converters.escape_string(
                str(v)
            )
            for v in temp
        ]
        sub_df_columns = [
            df_columns[j]
            for j in range(len(temp))
        ]
        update_sql = build_update_sql(
            sub_df_columns, value
        )
        # SQL 上傳資料方式
        # DUPLICATE KEY UPDATE 意思是
        # 如果有重複，就改用 update 的方式
        # 避免重複上傳
        sql = """INSERT INTO `{}`({})VALUES ({}) ON DUPLICATE KEY UPDATE {}
            """.format(
            table,
            "`{}`".format(
                "`,`".join(
                    sub_df_columns
                )
            ),
            '"{}"'.format(
                '","'.join(value)
            ),
            update_sql,
        )
        sql_list.append(sql)
    return sql_list


def df_update2mysql(
    df: pd.DataFrame,
    table: str,
    mysql_conn: engine.base.Connection,
):
    sql = build_df_update_sql(table, df)
    commit(
        sql=sql, mysql_conn=mysql_conn
    )


class MysqlDataBase:
    def __init__(self):
        self.router = Router()

    def df_update2mysql(
        self,
        df: pd.DataFrame,
        table: str,
    ):
        if len(df) > 0:
            # 直接上傳
            if upload_data(
                df=df,
                table=table,
                mysql_conn=self.router.mysql_financialdata_conn,
            ):
                pass
            else:
                # 如果有重複的資料
                # 使用 SQL 語法上傳資料
                df_update2mysql(
                    df,
                    table,
                    mysql_conn=self.router.mysql_financialdata_conn,
                )

    def create_table(self, table: str):
        sql = "SHOW TABLES"
        table_list = [
            x[0]
            for x in self.query(sql)
        ]
        if table in table_list:
            pass
        else:
            logger.info("create_table")
            sql = getattr(
                importlib.import_module(
                    f"financialdata.sql.{table}"
                ),
                "sql",
            )
            self.router.mysql_financialdata_conn.execute(
                sql
            )

    def get_max_date(self, table: str):
        try:
            sql = f"""
            SELECT max(date) FROM `{table}`
            """
            date = self.query(sql)
            if len(date) > 0:
                return date[0][
                    0
                ].strftime("%Y-%m-%d")
            else:
                return "2000-01-01"
        except Exception as e:
            return "2000-01-01"

    def query(
        self,
        sql: str,
    ):
        data = self.router.mysql_financialdata_conn.execute(
            sql
        )
        return data.fetchall()
