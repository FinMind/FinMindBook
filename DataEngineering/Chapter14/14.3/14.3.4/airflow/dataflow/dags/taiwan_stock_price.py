import airflow

from dataflow.constant import (
    DEFAULT_ARGS,
    MAX_ACTIVE_RUNS,
)
from dataflow.etl.taiwan_stock_price import (
    create_crawler_taiwan_stock_price_task,
)
from airflow.operators.dummy_operator import (
    DummyOperator,
)

with airflow.DAG(
    dag_id="taiwan_stock_price",
    default_args=DEFAULT_ARGS,
    # 設定每天 17:00 執行爬蟲
    schedule_interval="0 17 * * *",
    max_active_runs=MAX_ACTIVE_RUNS,
    # 設定參數，Airflow 除了按按鈕，單純的執行外
    # 也可以在按按鈕時，帶入特定參數
    # 在此設定 date 參數，讓讀者可自行輸入，想要爬蟲的日期
    params={
        "date (YYYY-MM-DD)": "",
    },
    catchup=False,
) as dag:
    start_task = DummyOperator(
        task_id="start_task"
    )
    end_task = DummyOperator(
        task_id="end_task"
    )
    crawler_taiwan_stock_price_task = (
        create_crawler_taiwan_stock_price_task()
    )
    (
        start_task
        >> crawler_taiwan_stock_price_task
        >> end_task
    )
