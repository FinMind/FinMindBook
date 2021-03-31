import time
import typing

import redis
from loguru import logger
from sqlalchemy import engine

from financialdata.backend.db import clients


def check_alive(connect: engine.base.Connection):
    connect.execute("SELECT 1 + 1")


def check_connect_alive(
    connect: typing.Union[engine.base.Connection, redis.Redis],
    connect_func: typing.Callable,
):
    if connect:
        try:
            check_alive(connect)
            return connect
        except Exception as e:
            logger.info(f"{connect_func.__name__} reconnect, error: {e}")
            time.sleep(1)
            try:
                connect = connect_func()
            except Exception as e:
                logger.info(f"{connect_func.__name__} connect error")
            return check_connect_alive(connect, connect_func)


class Router:
    def __init__(self):
        self._mysql_monitor_conn = clients.get_mysql_monitor_conn()
        self._mysql_financialdata_conn = clients.get_mysql_financialdata_conn()

    def check_mysql_monitor_conn_alive(self):
        self._mysql_monitor_conn = check_connect_alive(
            self._mysql_monitor_conn, clients.get_mysql_monitor_conn
        )
        return self._mysql_monitor_conn

    def check_mysql_financialdata_conn_alive(self):
        self._mysql_financialdata_conn = check_connect_alive(
            self._mysql_financialdata_conn, clients.get_mysql_financialdata_conn
        )
        return self._mysql_financialdata_conn

    @property
    def mysql_monitor_conn(self):
        return self.check_mysql_monitor_conn_alive()

    @property
    def mysql_financialdata_conn(self):
        return self.check_mysql_financialdata_conn_alive()
