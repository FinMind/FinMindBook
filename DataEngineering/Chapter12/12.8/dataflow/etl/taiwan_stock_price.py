import datetime

from airflow.operators.python_operator import (
    PythonOperator,
)

from dataflow.backend import db
from dataflow.crawler.taiwan_stock_price import (
    crawler,
)


def crawler_taiwan_stock_price_twse(
    **kwargs,
):
    # 由於在 DAG 層，設定 params，可輸入參數
    # 因此在此，使用以下 kwargs 方式，拿取參數
    # DAG 中 params 參數設定是 date (YYYY-MM-DD)
    # 所以拿取時，也要用一樣的字串
    params = kwargs["dag_run"].conf
    date = params.get(
        "date (YYYY-MM-DD)",
        # 如果沒有帶參數，則預設 date 是今天
        datetime.datetime.today().strftime(
            "%Y-%m-%d"
        ),
    )
    # 進行爬蟲
    df = crawler(
        dict(
            date=date,
            data_source="twse",
        )
    )
    # 資料上傳資料庫
    db.upload_data(
        df,
        "TaiwanStockPrice",
        db.router.mysql_financialdata_conn,
    )


def crawler_taiwan_stock_price_tpex(
    **kwargs,
):
    # 註解如上
    params = kwargs["dag_run"].conf
    date = params.get(
        "date (YYYY-MM-DD)",
        datetime.datetime.today().strftime(
            "%Y-%m-%d"
        ),
    )
    df = crawler(
        dict(
            date=date,
            data_source="tpex",
        )
    )
    db.upload_data(
        df,
        "TaiwanStockPrice",
        db.router.mysql_financialdata_conn,
    )


def create_crawler_taiwan_stock_price_task() -> PythonOperator:
    return [
        # 建立任務
        PythonOperator(
            task_id="taiwan_stock_price_twse",
            python_callable=crawler_taiwan_stock_price_twse,
            queue="twse",
            provide_context=True,
        ),
        PythonOperator(
            task_id="taiwan_stock_price_tpex",
            python_callable=crawler_taiwan_stock_price_tpex,
            queue="tpex",
            provide_context=True,
        ),
    ]
