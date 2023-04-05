import datetime
from functools import partial

from airflow.operators.python_operator import (
    PythonOperator,
)
from loguru import logger

from dataflow.backend import db
from dataflow.crawler.taiwan_stock_price import (
    crawler,
)


def crawler_taiwan_stock_price(
    **kwargs,
):
    data_source = kwargs["data_source"]
    params = kwargs["dag_run"].conf
    date = params.get(
        "date (YYYY-MM-DD)",
        datetime.datetime.today().strftime(
            "%Y-%m-%d"
        ),
    )
    logger.info(
        f"""
        data_source: {data_source}
        date: {date}
    """
    )
    df = crawler(
        dict(
            date=date,
            data_source=data_source,
        )
    )
    logger.info(df)
    db.upload_data(
        df,
        "TaiwanStockPrice",
        db.router.mysql_financialdata_conn,
    )
    logger.info("upload_data")


def create_crawler_taiwan_stock_price_task() -> PythonOperator:
    return [
        PythonOperator(
            task_id=f"taiwan_stock_price_{queue}",
            python_callable=partial(
                crawler_taiwan_stock_price,
                data_source=queue,
            ),
            queue=queue,
            provide_context=True,
        )
        for queue in ["twse", "tpex"]
    ]
