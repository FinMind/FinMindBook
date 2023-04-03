import airflow

from dataflow.constant import (
    CONCURRENCY,
    DEFAULT_ARGS,
    MAX_ACTIVE_RUNS,
)
from dataflow.etl.abcd import (
    create_a_task,
    create_b_task,
    create_c_task,
    create_d_task,
)

with airflow.DAG(
    dag_id="ABCD",
    default_args=DEFAULT_ARGS,
    schedule_interval=None,
    concurrency=CONCURRENCY,
    max_active_runs=MAX_ACTIVE_RUNS,
    catchup=False,
) as dag:
    task_a = create_a_task()
    task_b = create_b_task()
    task_c = create_c_task()
    task_d = create_d_task()
    task_a >> [task_b, task_c] >> task_d
