import importlib
import socket
import typing

import pymysql
from financialdata.backend import db
from celery import Celery, Task
from loguru import logger


class CallbackTask(Task):
    def retry(
        self, args: typing.List[typing.Union[str, typing.Dict[str, str]]]
    ):
        logger.info(f"retry: {args}")
        crawler_new = getattr(
            importlib.import_module("financialdata.tasks.task"), "crawler_new"
        )
        dataset = args[0]
        parameter = args[1]
        queue = args[2]
        task = crawler_new.s(dataset, parameter, queue)
        task.apply_async(queue=queue)

    def on_success(self, retval, task_id, args, kwargs):
        return super(CallbackTask, self).on_success(
            retval, task_id, args, kwargs
        )

    def on_failure(self, exc, task_id, args, kwargs, info):
        sql = """INSERT INTO `celery_log`(
                `retry`,`status`,`worker`, `task_id`, `msg`, `info`, `args`, `kwargs`)
                 VALUES ('0','-1', '{}', '{}', '{}', '{}', '{}', '{}')
        """.format(
            socket.gethostname(),
            task_id,
            pymysql.converters.escape_string(str(exc)),
            pymysql.converters.escape_string(str(info)),
            pymysql.converters.escape_string(str(args)),
            pymysql.converters.escape_string(str(kwargs)),
        )
        db.commit(sql=sql, mysql_conn=db.router.mysql_monitor_conn)
        self.retry(args)
        return super(CallbackTask, self).on_failure(
            exc, task_id, args, kwargs, info
        )


app = Celery(
    "tasks",
    include="financialdata.tasks.task",
    # backend='rpc://',
    broker='pyamqp://worker:worker@localhost:5672/',
)
