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
    # 由於在 DAG 層，設定 params，可輸入參數
    data_source = kwargs["data_source"]
    params = kwargs["dag_run"].conf
    # 因此在此，使用以上 kwargs 方式，拿取參數
    # DAG 中 params 參數設定是 date (YYYY-MM-DD)
    # 所以拿取時，也要用一樣的字串
    date = params.get(
        "date (YYYY-MM-DD)",
        # 如果沒有帶參數，則預設 date 是今天
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
    # 進行爬蟲
    df = crawler(
        dict(
            date=date,
            data_source=data_source,
        )
    )
    logger.info(df)
    # 資料上傳資料庫
    db.upload_data(
        df,
        "TaiwanStockPrice",
        db.router.mysql_financialdata_conn,
    )
    logger.info("upload_data")


def create_crawler_taiwan_stock_price_task() -> PythonOperator:
    return [
        # 用 for 迴圈建立任務
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
