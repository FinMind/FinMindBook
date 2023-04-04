import airflow
from airflow.operators.dummy_operator import (
    DummyOperator,
)
from dataflow.constant import (
    DEFAULT_ARGS,
    MAX_ACTIVE_RUNS,
)
from dataflow.etl.dummy_operator import (
    create_crawler1_task,
    create_crawler2_task,
    create_crawler3_task,
    create_stock_strategy_task,
)

with airflow.DAG(
    dag_id="DummyOperator",
    default_args=DEFAULT_ARGS,
    schedule_interval=None,
    max_active_runs=MAX_ACTIVE_RUNS,
    catchup=False,
) as dag:
    crawler_task = DummyOperator(
        task_id="crawler_task"
    )
    strategy_task = DummyOperator(
        task_id="strategy_task"
    )
    (
        crawler_task
        >> [
            create_crawler1_task(),
            create_crawler2_task(),
            create_crawler3_task(),
        ]
        >> strategy_task
        >> create_stock_strategy_task()
    )
